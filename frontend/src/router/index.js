import { createRouter, createWebHistory } from 'vue-router'
import TimelineView from '../views/TimelineView.vue'
import PeopleView from '../views/PeopleView.vue'
import ChatView from '../views/ChatView.vue'
import ProfileView from '../views/ProfileView.vue'
import PersonDetailView from '../views/PersonDetailView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  { path: '/', redirect: '/timeline' },
  { path: '/timeline', name: 'timeline', component: TimelineView },
  { path: '/people', name: 'people', component: PeopleView },
  { path: '/chat', name: 'chat', component: ChatView },
  { path: '/profile', name: 'profile', component: ProfileView },
  { path: '/person/:id', name: 'person-detail', component: PersonDetailView },
  { path: '/settings', name: 'settings', component: SettingsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
