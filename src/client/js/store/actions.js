import * as types from './mutation-types'

export default {
  setHeaderMenuOpen: (ctx, isOpen) => {
    ctx.commit(types.SET_COMMON_HEADER_MENU_OPEN, isOpen)
  },

  setLoading: (ctx, isLoading) => {
    ctx.commit(types.SET_COMMON_LOADING, isLoading)
  },

  setAdminUser: async (ctx, payload) => {
    ctx.commit(types.SET_ADMIN_USER, payload)
  },

  setCategoryItems: async (ctx, payload) => {
    ctx.commit(types.SET_CATEGORY_ITEMS, payload)
  },

  pushItemToAdminPostsPagerKeys: async (ctx, payload) => {
    ctx.commit(types.PUSH_ITEM_TO_ADMIN_POSTS_PAGER_KEYS, payload)
  },

  resetAdminPostsPager: async (ctx, isResetKeys = false) => {
    ctx.commit(types.RESET_ADMIN_POSTS_PAGER, isResetKeys)
  },

  setAdminPostsPagerLastIndex: async (ctx, payload) => {
    ctx.commit(types.SET_ADMIN_POSTS_PAGER_LAST_INDEX, payload)
  },

  setAdminPostsPagerParams: async (ctx, payload) => {
    ctx.commit(types.SET_ADMIN_POSTS_PAGER_PARAMS, payload)
  },

  pushItemToAdminShortenUrlsPagerKeys: async (ctx, payload) => {
    ctx.commit(types.PUSH_ITEM_TO_ADMIN_SHORTEN_URLS_PAGER_KEYS, payload)
  },

  resetAdminShortenUrlsPager: async (ctx, isResetKeys = false) => {
    ctx.commit(types.RESET_ADMIN_SHORTEN_URLS_PAGER, isResetKeys)
  },

  setAdminShortenUrlsPagerLastIndex: async (ctx, payload) => {
    ctx.commit(types.SET_ADMIN_SHORTEN_URLS_PAGER_LAST_INDEX, payload)
  },
}

