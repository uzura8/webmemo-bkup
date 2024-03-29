import traceback
from flask import jsonify, request
from flask_cognito import cognito_auth_required, current_cognito_jwt
from app.models.dynamodb import PostGroup, Post, ModelInvalidParamsException
from app.common.error import InvalidUsage
from app.common.date import utc_iso
from app.common.request import validate_req_params
from app.validators import NormalizerUtils
from app.admin import bp, site_before_request, check_acl_service_id, admin_role_editor_required

reserved_slugs = PostGroup.get_reserved_values('slug')

@bp.before_request
@site_before_request
def before_request():
    pass


@bp.route('/posts/<string:service_id>/groups', methods=['POST', 'GET'])
@cognito_auth_required
@admin_role_editor_required
def post_group_list(service_id):
    check_acl_service_id(service_id)

    if request.method == 'POST':
        schema = validation_schema_group_list_post()
        vals = validate_req_params(schema, request.json)
        vals['serviceId'] = service_id
        vals['serviceIdSlug'] = '#'.join([service_id, vals['slug']])
        vals['updatedAt'] = utc_iso(False, True)
        created_by = current_cognito_jwt.get('cognito:username', '')
        if created_by:
            vals['createdBy'] = created_by

        try:
            group = PostGroup.create(vals)

        except ModelInvalidParamsException as e:
            raise InvalidUsage(e.message, 400)

        except Exception as e:
            print(traceback.format_exc())
            raise InvalidUsage('Server Error', 500)

    else:
        params = {}
        for key in ['count', 'order']:
            params[key] = request.args.get(key)
        vals = validate_req_params(validation_schema_group_list_get(), params)
        pkeys = {'key':'serviceId', 'val':service_id}
        res = PostGroup.get_all_by_pkey(pkeys, vals, 'PostGroupsByServiceIdGsi')
        group = [ PostGroup.to_response(item) for item in res ]

    return jsonify(group), 200


@bp.route('/posts/<string:service_id>/groups/slug', methods=['GET'])
@cognito_auth_required
@admin_role_editor_required
def post_group_detail_slug(service_id):
    check_acl_service_id(service_id)
    params = {}
    for key in ['checkNotExists', 'slug', 'withPostDetail']:
        params[key] = request.args.get(key)
    vals = validate_req_params(validation_schema_group_detail_slug_get(), params)

    item = PostGroup.get_one_by_pkey('serviceIdSlug', '#'.join([service_id, vals['slug']]))
    is_not_exists = not item
    return jsonify(is_not_exists), 200


@bp.route('/posts/<string:service_id>/groups/<string:slug>',
          methods=['POST', 'GET', 'HEAD', 'DELETE'])
@cognito_auth_required
@admin_role_editor_required
def post_group_detail(service_id, slug):
    check_acl_service_id(service_id)
    query_key = '#'.join([service_id, slug])
    group = PostGroup.get_one_by_pkey('serviceIdSlug', query_key)

    saved = None
    if request.method == 'POST':
        vals = validate_req_params(validation_schema_group_list_post(), request.json)
        vals['serviceId'] = service_id
        vals['updatedBy'] = current_cognito_jwt.get('cognito:username', '')

        try:
            query_keys = {'p': {'key':'serviceIdSlug', 'val':query_key}}
            saved = PostGroup.update(query_keys, vals)

        except ModelInvalidParamsException as e:
            raise InvalidUsage(e.message, 400)

        except Exception as e:
            print(traceback.format_exc())
            raise InvalidUsage('Server Error', 500)

        if not saved:
            saved = group

    elif request.method == 'DELETE':
        PostGroup.delete({'serviceIdSlug':query_key})
        return jsonify(), 200

    if request.method == 'HEAD':
        return jsonify(), 200

    else:
        vals = validate_req_params(validation_schema_group_detail_get(),
                                   {'withPostDetail':request.args.get('withPostDetail')})
        if vals.get('withPostDetail'):
            posts = []
            if group.get('postIds'):
                keys = [ {'postId':pid} for pid in group['postIds'] ]
                batch_res = Post.batch_get_items(keys)
                for pid in group['postIds']:
                    p = next((p for p in batch_res if p.get('postId') == pid), None)
                    if p:
                        posts.append(p)
            group['posts'] = posts

    res = saved if saved else group
    return jsonify(res), 200


def validation_schema_group_list_post():
    return {
        'slug': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'maxlength': 128,
            'regex': r'^[0-9a-z\-]+$',
            'valid_ulid': False,
            'forbidden': reserved_slugs,
        },
        'label': {
            'type': 'string',
            'coerce': (NormalizerUtils.trim),
            'required': True,
            'empty': False,
        },
        'postIds' : {
            'type': 'list',
            'required': False,
            'schema': {
                'type': 'string',
                'coerce': (NormalizerUtils.trim),
            }
        },
    }


def validation_schema_group_list_get():
    return {
        'count': {
            'type': 'integer',
            'coerce': int,
            'required': False,
            'min': 1,
            'max': 50,
            'default': 20,
        },
        'order': {
            'type': 'string',
            'required': False,
            'allowed': ['asc', 'desc'],
            'default': 'desc',
        },
    }


def validation_schema_group_detail_get():
    return {
        'withPostDetail': {
            'type': 'boolean',
            'coerce': (str, NormalizerUtils.to_bool),
            'required': False,
            'nullable': True,
            'empty': True,
            'default': False,
        },
    }


def validation_schema_group_detail_slug_get():
    return {
        'slug': {
            'type': 'string',
            'coerce': (str, NormalizerUtils.trim),
            'required': True,
            'empty': False,
            'maxlength': 128,
            'regex': r'^[0-9a-z\-]+$',
            'valid_ulid': False,
            'forbidden': reserved_slugs,
        },
        'checkNotExists': {
            'type': 'boolean',
            'coerce': (str, NormalizerUtils.to_bool),
            'required': True,
            'empty': False,
            'default': False,
        },
    }
