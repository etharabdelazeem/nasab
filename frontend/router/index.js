import { createRouter, createWebHistory } from 'vue-router';
import Onboarding from '../views/Onboarding.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';
import Search from '../views/Search.vue';
import SearchResult from '../views/SearchResult.vue';
import AddFamilyMember from '../views/AddFamilyMember.vue';
import UserProfile from '../views/UserProfile.vue';

const routes = [
  { path: '/', component: Onboarding },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/dashboard', component: Dashboard },
  { path: '/search', component: Search },
  { path: '/search-result', component: SearchResult },
  { path: '/add-family-member', component: AddFamilyMember },
  { path: '/user-profile', component: UserProfile },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
