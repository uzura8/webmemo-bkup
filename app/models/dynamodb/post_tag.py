from boto3.dynamodb.conditions import Key
from app.common.date import utc_iso
from app.models.dynamodb.base import Base
from app.models.dynamodb.tag import Tag


class PostTag(Base):
    table_name = 'post-tag'
    public_attrs = [
        'postId',
        'tagId',
        'publishAt',
        'statusPublishAt',
    ]
    response_attrs = public_attrs + []
    private_attrs = []
    all_attrs = public_attrs + private_attrs


    @classmethod
    def get_all_by_post_id(self, post_id, with_tags=False, for_response=True):
        table = self.get_table()
        res = table.query(
            KeyConditionExpression=Key('postId').eq(post_id),
            ScanIndexForward=True
        )
        items = res.get('Items', [])
        if not items:
            return []

        if not with_tags:
            return [ self.to_response(i) for i in items ] if for_response else items

        keys = []
        for item in items:
            keys.append({'tagId':item['tagId']})
        items = Tag.batch_get_items(keys)
        return [ Tag.to_response(i) for i in items ] if for_response else items


    @classmethod
    def query_pager_published_by_tag_id(self, tag_id, params):
        #until_time = params.get('untilTime', '')
        #since_time = params.get('sinceTime', '')
        is_desc = params.get('order', 'asc') == 'desc'
        limit = params.get('count', 20)
        start_key = params.get('pagerKey')

        status = 'publish'
        exp_attr_names = {}
        exp_attr_vals = {}
        key_conds = ['#ti = :ti']
        option = {
            'IndexName': 'postsByTagGsi',
            'ProjectionExpression': self.prj_exps_str(),
            'ScanIndexForward': not is_desc,
        }
        exp_attr_names['#ti'] = 'tagId'
        exp_attr_vals[':ti'] = tag_id

        #current = utc_iso(False, True)
        #if not until_time or until_time > current:
        #    until_time = current

        key_conds.append('begins_with(#sp, :sp)')
        exp_attr_names['#sp'] = 'statusPublishAt'
        exp_attr_vals[':sp'] = status

        filter_exps = []
        #if since_time:
        #    cond = '#st > :st'
        #    exp_attr_names['#st'] = sort_key
        #    exp_attr_vals[':st'] = since_time
        #    filter_exps.append(cond)

        current = utc_iso(False, True)
        cond = '#ut < :ut'
        exp_attr_names['#ut'] = 'publishAt'
        exp_attr_vals[':ut'] = current
        filter_exps.append(cond)

        filter_exps_str = ' AND '.join(filter_exps) if filter_exps else ''
        filter_exp = ''
        if filter_exps_str:
            filter_exp += filter_exps_str

        if filter_exp:
            option['FilterExpression'] = filter_exp

        option['KeyConditionExpression'] = ' AND '.join(key_conds)
        option['ExpressionAttributeNames'] = exp_attr_names
        option['ExpressionAttributeValues'] = exp_attr_vals

        pager_keys = {'pkey':'postId', 'index_pkey':'tagId', 'index_skey':'statusPublishAt'}
        items, pager_key = self.query_loop_for_limit(option, limit, start_key, pager_keys)

        return {
            'items': items,
            'pagerKey': pager_key
        }
