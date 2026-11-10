import { createRouter, createWebHistory } from 'vue-router' 
import home from '../views/home.vue'
import AdminDashboard from '../views/admin-dashboard.vue'
import StaffDashboard from '../views/staff-dashboard.vue'
import TrekkerDashboard from '../views/trekker-dashboard.vue'
import AdminManageTrekkingStaff from '../components/admin-trekking-staff.vue'
import TrekkerRegistration from '../components/trekker-registration.vue'
import AdminManageTrekkers from '../components/admin-trekkers.vue'
import AdminManageTreks from '../components/admin-treks.vue'
import AdminManageBookings from '../components/admin-bookings.vue'
import StaffManageTreks from '../components/staff-treks.vue'
import StaffManageParticipants from '../components/staff-participants.vue'
import StaffProfile from '../components/staff-profile.vue'
import TrekkerBrowseTreks from '../components/trekker-browse-treks.vue'
import TrekkerBookings from '../components/trekker-bookings.vue'
import TrekkerHistory from '../components/trekker-history.vue'
import TrekkerProfile from '../components/trekker-profile.vue'

const routes = [
  {path: '/', name: 'Home', component: home},
  {path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard},
  {path: '/staff/dashboard', name: 'StaffDashboard', component: StaffDashboard},
  {path: '/trekker/dashboard', name: 'TrekkerDashboard', component: TrekkerDashboard},
  {path: '/admin/trekking-staff', name: 'AdminManageTrekkingStaff', component: AdminManageTrekkingStaff},
  {path: '/trekker/registration', name: 'TrekkerRegistration', component: TrekkerRegistration},
  {path: '/admin/trekkers', name: 'AdminManageTrekkers', component: AdminManageTrekkers},
  {path: '/admin/treks', name: 'AdminManageTreks', component: AdminManageTreks},
  {path: '/admin/bookings', name: 'AdminManageBookings', component: AdminManageBookings},
  {path: '/staff/treks', name: 'StaffManageTreks', component: StaffManageTreks},
  {path: '/staff/participants', name: 'StaffManageParticipants', component: StaffManageParticipants},
  {path: '/staff/profile', name: 'StaffProfile', component: StaffProfile},
  {path: '/trekker/browse-treks', name: 'TrekkerBrowseTreks', component: TrekkerBrowseTreks},
  {path: '/trekker/bookings', name: 'TrekkerBookings', component: TrekkerBookings},
  {path: '/trekker/history', name: 'TrekkerHistory', component: TrekkerHistory},
  {path: '/trekker/profile', name: 'TrekkerProfile', component: TrekkerProfile}
]

const router = createRouter({history: createWebHistory(), routes})
export default router