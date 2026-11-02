import { createRouter, createWebHistory } from 'vue-router' 
import home from '../views/home.vue'
import AdminDashboard from '../views/admin-dashboard.vue'
import StaffDashboard from '../views/staff-dashboard.vue'
import TrekkerDashboard from '../views/trekker-dashboard.vue'
import AdminManageTrekkingStaff from '../components/admin-trekking-staff.vue'
import TrekkerRegistration from '../components/trekker-registration.vue'

const routes = [
  {path: '/', name: 'Home', component: home},
  {path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard},
  {path: '/staff-dashboard', name: 'StaffDashboard', component: StaffDashboard},
  {path: '/trekker-dashboard', name: 'TrekkerDashboard', component: TrekkerDashboard},
  {path: '/admin/trekking-staff', name: 'AdminManageTrekkingStaff', component: AdminManageTrekkingStaff},
  {path: '/trekker-registration', name: 'TrekkerRegistration', component: TrekkerRegistration}
]

const router = createRouter({history: createWebHistory(), routes})
export default router