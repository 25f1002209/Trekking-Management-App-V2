<template>
  <div class="brand">
    <div>
        <h1>Treknologia</h1>
        <h4>Explore the unexplored</h4>
    </div>
    <div class="admin-profile"><div class="profile-icon">👤</div><span>{{ user.name }}</span></div>
  </div>
  <div class="dashboard">
    <aside class="sidebar">
      <div class="sidebar-menu">
        <div v-for="item in menuItems" :key="item.name" class="menu-item" :class="{ active: activeMenu === item.name }" @click="selectMenu(item)">
          <span class="menu-symbol">{{ item.icon }}</span>
          <span>{{ item.name }}</span>
        </div>
        <div class="menu-item" style="margin-top: 302px;" @click="logout"><span class="menu-symbol">⇥</span><span>Logout</span></div>
      </div>
    </aside>
    <div class="main-section" :class="{ expanded: sidebarHidden }">
      <main class="dashboard-content">
        <div v-if="loading" class="message">
          Loading available treks...
        </div>
        <div v-else-if="error" class="message error-message">
          {{ error }}
          <button @click="fetchBookingdData">Retry</button>
        </div>
        <div class="bookings-section">
          <h1>My Bookings</h1>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Trek Name</th>
                  <th>Booking Date</th>
                  <th>Trek Dates</th>
                  <th>Payment Status</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="booking in bookings" :key="booking.id">
                  <td>{{ booking.trek_name }}</td>
                  <td>{{ booking.booking_date }}</td>
                  <td>{{ booking.trek_dates }}</td>
                  <td><span class="status" :class="booking.payment_status">{{ booking.payment_status }}</span></td>
                  <td><span class="status" :class="booking.status">{{ booking.status }}</span></td>
                </tr>
                <tr v-if="bookings.length === 0">
                  <td colspan="5" class="empty-message">
                    You haven't made any bookings yet.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import trekkingImage from "../assets/trekking.jpg";
export default {
  name: "TrekkerBookings",
  data() {
    return {
      user: { id: null, name: "", email: "" },
      bookings: [],
      loading: false,
      error: "",
      activeMenu: "My Bookings",
      menuItems: [
        { name: "Dashboard", icon: "⌂", path: "/trekker/dashboard" },
        { name: "Browse Treks", icon: "♧", path: "/trekker/browse-treks" },
        { name: "My Bookings", icon: "▣", path: "/trekker/bookings" },
        { name: "History", icon: "◉", path: "/trekker/history" },
        { name: "Profile", icon: "♙", path: "/trekker/profile" }
      ]
    };
  },
  computed: {
    filteredTreks() {
      return this.treks.filter(trek => {
        const difficultyMatch = this.selectedDifficulty === "All" || trek.difficulty === this.selectedDifficulty;
        const locationMatch = this.selectedLocation === "All" || trek.location === this.selectedLocation;
        return difficultyMatch && locationMatch;
      });
    },
    locations() {
      return [...new Set(this.treks.map(trek => trek.location).filter(Boolean))];
    }
  },
  mounted() {
    this.fetchBookingData();
  },
  methods: {
    async fetchBookingData() {
      this.loading = true;
      this.error = "";
      try {
        const response = await axios.get("http://localhost:5000/api/trekker/bookings", { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
        const data = response.data;
        if (data.success) {
          this.user = data.user;
          this.bookings = data.bookings || [];
        }
      } catch (error) {
        console.error("Trekker Dashboard Error:", error.response?.data || error);
        this.error = error.response?.data?.message || "Unable to load dashboard.";
      } finally {
        this.loading = false;
      }
    },
    getTrekImage(trek) {
      if (trek.photo) {
        return trek.photo.startsWith("http") ? trek.photo : `http://localhost:5000/${trek.photo.replace(/^\/+/, "")}`;
      }
      return trekkingImage;
    },
    formatDate(date) {
      if (!date) return "-";
      const parts = date.split("-");
      if (parts.length !== 3) return date;
      return `${parts[2]} ${new Date(Number(parts[0]), Number(parts[1]) - 1).toLocaleString("en-US", { month: "short" })} ${parts[0]}`;
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/");
    },
    selectMenu(item) {
      this.activeMenu = item.name;
      if (item.path !== this.$route.path) {
        this.$router.push(item.path);
      }
    }
  }
};
</script>

<style scoped>
* {box-sizing: border-box;}
html, body {
    margin: 0;
    min-height: 100%;
    overflow-y: auto;
}
#app {
    min-height: 100vh;
}
.brand {
    top: 0;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 5px 0px;
    background: rgba(184, 214, 250, 0.9);
    border-bottom: 1px solid rgba(8, 8, 8, 0.25);
}
.brand h1 {
    margin: 0;
    font-size: 30px;
    padding: 0px 30px;
    font-weight: bold;
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
    color: #00027f;
    text-align: left;
}
.brand h4 {
    margin: 0;
    font-size: 15px;
    padding: 0px 35px;
    font-weight: bold;
    font-family: Arial, Helvetica, sans-serif;
    font-style: italic;
    color: #00027f;
    text-align: left;
}
.admin-profile {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    align-content: center; margin-left: auto; margin-right: 80px; font-weight: 700; font-family: sans-serif; font-size: large;
}
.profile-icon {
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #540084;
    border-radius: 50%;
    font-size: 24px;
}
.dashboard {
    display: flex;
    width: 100%;
    min-height: 100vh;
    font-family: Arial, Helvetica, sans-serif;
    color: #111827;
    background: #ffffff;
}
.sidebar {
    width: 240px;
    min-width: 205px;
    min-height: 100vh;
    border-right: 2px solid #e2e8f0;
    background: #0050c0;
    padding: 10px 12px;
}
.menu-icon {
    height: 55px;
    display: flex;
    align-items: center;
    padding: 0 25px;
    border-bottom: 2px solid #e2e8f0;
    font-size: 25px;
    cursor: pointer;
}
.sidebar-menu {
    padding: 10px 5px;
}
.menu-item {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 14px 12px;
    margin-bottom: 15px;
    border-radius: 8px;
    font-size: 20px;
    font-weight: 600;
    cursor: pointer;
    color:#cbd5e1;
}
.menu-item:hover {
    background: #add6ff;
    color: #0b58f0;
}
.menu-item.active {
    color: #155eef;
    background: #e8f0ff;
}
.menu-symbol {
    width: 23px;
    text-align: center;
    font-size: 21px;
    flex-shrink: 0;
}
.main-section {
    flex: 1;
    min-width: 0;
}
.staff-profile {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    font-weight: 600;
}
.dashboard-content {
    padding: 25px 22px;
}
.dashboard-content h1 {
    margin: 0 0 27px;
    font-size: 28px;
    font-weight: 700;
}
.stats-container {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 35px;
}

.stat-card {
    min-height: 140px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 20px;
    border: 2px solid #e2e8f0;
    border-radius: 11px;
    background: #ffffff;
    box-shadow: 0 2px 5px rgba(15, 23, 42, 0.04);
}

.stat-card h3 {
    margin: 0 0 12px;
    font-size: 15px;
    line-height: 1.4;
    font-weight: 700;
}

.stat-card p {
    margin: 0;
    font-size: 31px;
    font-weight: 700;
}

.stat-icon {
    font-size: 38px;
    color: #111827;
}

.treks-section h2 {
    margin: 0 0 18px;
    font-size: 21px;
    font-weight: 700;
}

.table-container {
    width: 100%;
    overflow-x: auto;
    border: 2px solid #e2e8f0;
    border-radius: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    white-space: nowrap;
}

thead {
    background: #c5e7ff;
}

th {
    padding: 13px 10px;
    font-size: 13px;
    font-weight: 700;
}

td {
    padding: 12px 9px;
    font-size: 12px;
    border-top: 1px solid #e2e8f0;
}

tbody tr:hover {
    background: #f8fafc;
}

.status {
    font-weight: 600;
}

.status.Open {
    color: #15803d;
}
.status.Upcoming {
    color: #f97316;
}
.status.Closed {
    color: #dc2626;
}
.status.Cancelled {
    color: #dc2626;
}
.status.Pending{
    color: #f97316;
}
.status.Confirmed{
    color: #15803d
}
.status.Completed{
    color: #15803d
}
.empty-message {
    padding: 25px;
    text-align: center;
    color: #64748b;
}

.message {
    padding: 20px;
    color: #475569;
}

.error-message {
    padding: 16px;
    border: 1px solid #fecaca;
    border-radius: 8px;
    background: #fef2f2;
    color: #b91c1c;
}
.trek-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 16px;
    margin-top: 20px;
}

.trek-card {
    background: white;
    border: 1px solid #dbe2ea;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.trek-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}

.trek-details {
    padding: 12px;
    display: flex;
    flex-direction: column;
    flex: 1;
}

.trek-details h3 {
    font-size: 15px;
    font-weight: 600;
    color: #111827;
    margin: 0 0 2px;
    padding: 2px 5px;
}

.trek-details p {
    font-size: 15px;
    color: #374151;
    margin: 0 0 0px;
    line-height: 1.4;
    padding: 0px 5px;
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    font-weight: 500;
}

.outline-button {
    width: 100%;
    padding: 10px;
    margin-top:10px;
    background: white;
    color: #155eef;
    border: 2px solid #93b4ff;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

.outline-button:hover {
    background: #eff6ff;
    border-color: #155eef;
}

.unavailable-button {
    width: 100%;
    padding: 10px;
    margin-top: auto;
    background: #f9fafb;
    color: #374151;
    border: 2px solid #d1d5db;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    cursor: not-allowed;
}

@media (max-width: 900px) {
    .trek-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 600px) {
    .trek-grid {
        grid-template-columns: 1fr;
    }
}

.error-message button {
    margin-left: 12px;
    padding: 6px 12px;
    border: 1px solid #b91c1c;
    border-radius: 5px;
    background: #ffffff;
    color: #b91c1c;
    cursor: pointer;
}
.view-all {
    display: flex;
    justify-content: flex-end;
    margin-top: 35px;
}
.view-all button {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 5px 10px;
    border: none;
    background: transparent;
    color: #155eef;
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
}
.view-all button:hover {
    text-decoration: underline;
}

.view-all span {
    font-size: 25px;
}

@media (max-width: 1100px) {
    .stats-container {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 760px) {
    .sidebar {
        width: 65px;
        min-width: 65px;
    }

    .menu-icon {
        justify-content: center;
        padding: 0;
    }

    .menu-item {
        justify-content: center;
        padding: 12px 5px;
    }

    .menu-item span:last-child {
        display: none;
    }

    .topbar {
        padding: 0 12px;
    }

    .topbar h3 {
        font-size: 13px;
    }

    .staff-profile {
        gap: 5px;
        font-size: 12px;
    }

    .dashboard-content {
        padding: 20px 12px;
    }

    .dashboard-content h1 {
        font-size: 23px;
    }

    .stats-container {
        grid-template-columns: 1fr;
    }

    .stat-card {
        min-height: 95px;
    }

    .treks-section h2 {
        font-size: 19px;
    }

    th,
    td {
        padding: 12px 8px;
    }
}
</style>