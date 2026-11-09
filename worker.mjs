import {onRequest} from './functions/api/inquiries.js';

export default {
  fetch(request, env, ctx) {
    if (new URL(request.url).pathname === '/api/inquiries') {
      return onRequest({request, env, waitUntil: ctx.waitUntil.bind(ctx)});
    }
    return env.ASSETS.fetch(request);
  },
};
