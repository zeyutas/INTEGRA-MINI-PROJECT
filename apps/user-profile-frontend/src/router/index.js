import Vue from 'vue';
import Router from 'vue-router';
import Login from '../views/Login.vue';
import Profile from '../views/Profile.vue';
import { isAuthenticated } from '../services/auth';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: Login },
    { path: '/profile', name: 'Profile', component: Profile }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.path === '/login') {
    if (isAuthenticated()) {
      next('/profile');
    } else {
      next();
    }
    return;
  }

  if (!isAuthenticated()) {
    next('/login');
    return;
  }

  next();
});
//test
export default router;
