<template>
  <div class="dashboard">

    <aside class="sidebar">
      <div class="menu-icon">☰</div>
      <div class="sidebar-menu">
        <div v-for="item in menuItems" :key="item.name" class="menu-item" :class="{ active: activeMenu === item.name }"
          @click="selectMenu(item)">
          <span class="menu-symbol">{{ item.icon }}</span>
          <span>{{ item.name }}</span>
        </div>
      </div>
    </aside>
    <div class="main-section">
      <header class="topbar">
        <h3>Trekking Management Application</h3>
        <div class="profile">
          <span class="profile-icon">♙</span>
          <span>{{ user.name || 'Trekker' }}</span>
          <span>⌄</span>
        </div>
      </header>
      <main class="dashboard-content">
        <h1>Welcome, {{ user.name || 'Trekker' }}!</h1>
        <div class="section-heading">
          <h2>Available Treks</h2>
          <div class="filters">
            <select v-model="selectedDifficulty">
              <option value="All">Difficulty: All</option>
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
            <select v-model="selectedLocation">
              <option value="All">Location: All</option>
              <option v-for="location in locations" :key="location" :value="location">
                {{ location }}
              </option>
            </select>
          </div>
        </div>
        <div v-if="loading" class="message">
          Loading available treks...
        </div>
        <div v-else-if="error" class="message error-message">
          {{ error }}
          <button @click="fetchDashboardData">Retry</button>
        </div>
        <div v-else class="trek-grid">
          <div v-for="trek in filteredTreks" :key="trek.id" class="trek-card">
            <img :src="getTrekImage(trek)" alt="Trek Image" class="trek-image" />
            <div class="trek-details">
              <h3>{{ trek.name }}</h3>
              <p>{{ trek.location }}</p>
              <p>{{ trek.difficulty }} - {{ trek.duration }} Days</p>
              <p>Slots Left: {{ trek.available_slots }}</p>
              <button v-if="trek.available_slots > 0" class="outline-button" @click="bookTrek(trek)">
                Book Now
              </button>
              <button v-else class="unavailable-button" disabled>
                Not Available
              </button>
            </div>
          </div>
          <div v-if="filteredTreks.length === 0" class="empty-message">
            No treks available for the selected filters.
          </div>
        </div>
        <div class="bookings-section">
          <h2>My Bookings</h2>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Trek Name</th>
                  <th>Booking Date</th>
                  <th>Trek Dates</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="booking in bookings" :key="booking.id">
                  <td>{{ booking.trek_name }}</td>
                  <td>{{ formatDate(booking.booking_date) }}</td>
                  <td>{{ formatDate(booking.start_date) }} - {{ formatDate(booking.end_date) }}</td>
                  <td><span class="booking-status" :class="booking.status.toLowerCase()">{{ booking.status }}</span>
                  </td>
                  <td>
                    <button class="view-button" @click="viewBooking(booking)">
                      View Details
                    </button>
                  </td>
                </tr>
                <tr v-if="bookings.length === 0">
                  <td colspan="5" class="empty-message">
                    You haven't made any bookings yet.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="view-all">
            <span @click="selectMenu({ name: 'My Bookings', path: '/trekker-bookings' })">
              View All Bookings &nbsp; →
            </span>
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
  name: "TrekkerDashboard",
  data() {
    return {
      user: { id: null, name: "", email: "" },
      treks: [],
      bookings: [],
      loading: false,
      error: "",
      selectedDifficulty: "All",
      selectedLocation: "All",
      activeMenu: "Dashboard",
      menuItems: [
        { name: "Dashboard", icon: "⌂", path: "/trekker-dashboard" },
        { name: "Browse Treks", icon: "♧", path: "/trekker-browse-treks" },
        { name: "My Bookings", icon: "▣", path: "/trekker-bookings" },
        { name: "History", icon: "◉", path: "/trekker-history" },
        { name: "Profile", icon: "♙", path: "/trekker-profile" },
        { name: "Logout", icon: "⇥", path: "/" }
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
    this.fetchDashboardData();
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true;
      this.error = "";
      try {
        const response = await axios.get("http://localhost:5000/api/trekker-dashboard", { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
        const data = response.data;
        if (data.success) {
          this.user = data.user;
          this.treks = data.treks || [];
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
    async bookTrek(trek) {
      this.$router.push({path: "/trekker-browse-treks", query: {trek_id: trek.id}});
    },
    viewBooking(booking) {
      this.$router.push({
        path: "/trekker-bookings",
        query: {
          booking_id: booking.id
        }
      });
    },
    selectMenu(item) {
      this.activeMenu = item.name;
      if (item.name === "Logout") {
        localStorage.removeItem("token");
        this.$router.push("/");
      } else if (item.path !== this.$route.path) {
        this.$router.push(item.path);
      }
    }
  }
};
</script>

<style scoped>
* {box-sizing: border-box;}
.dashboard {
  display: flex;
  width: 100%;
  min-height: 100vh;
  font-family: Arial, Helvetica, sans-serif;
  color: #111827;
  background: #ffffff;
}
.sidebar {
  width: 205px;
  min-width: 205px;
  min-height: 100vh;
  border-right: 2px solid #e2e8f0;
  background: #ffffff;
}
.menu-icon {
  height: 65px;
  display: flex;
  align-items: center;
  padding: 0 25px;
  border-bottom: 2px solid #e2e8f0;
  font-size: 25px;
}
.sidebar-menu {padding: 14px 5px;}
.menu-item {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 14px 12px;
  margin-bottom: 5px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}
.menu-item:hover {background: #f1f5f9;}
.menu-item.active {
  color: #155eef;
  background: #e8f0ff;
}
.menu-symbol {
  width: 23px;
  text-align: center;
  font-size: 21px;
}
.main-section {
  flex: 1;
  min-width: 0;
}
.topbar {
  height: 65px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 25px;
  border-bottom: 2px solid #e2e8f0;
  background: #ffffff;
}
.topbar h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
}
.profile {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 600;
}
.profile-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #cbd5e1;
  border-radius: 50%;
  font-size: 24px;
}
.dashboard-content {padding: 22px 18px;}
.dashboard-content h1 {
  margin: 0 0 22px;
  font-size: 22px;
  font-weight: 700;
}
.dashboard-content h2 {
  margin: 0;
  font-size: 19px;
  font-weight: 700;
}
.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 16px;
}
.filters {
  display: flex;
  gap: 12px;
}
.filters select {
  min-width: 125px;
  height: 39px;
  padding: 0 10px;
  border: 2px solid #e2e8f0;
  border-radius: 7px;
  background: #ffffff;
  font-size: 13px;
  outline: none;
}
.trek-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 28px;
}
.trek-card {
  min-width: 0;
  overflow: hidden;
  border: 2px solid #e2e8f0;
  border-radius: 9px;
  background: #ffffff;
}
.trek-image {
  width: 100%;
  height: 125px;
  display: block;
  object-fit: cover;
}
.trek-details {padding: 10px;}
.trek-details h3 {
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 700;
}
.trek-details p {
  margin: 0 0 10px;
  font-size: 13px;
  color: #374151;
}
.outline-button {
  width: 100%;
  height: 37px;
  margin-top: 3px;
  border: 2px solid #8bb5ff;
  border-radius: 6px;
  background: #ffffff;
  color: #155eef;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}
.outline-button:hover {background: #eff6ff;}
.unavailable-button {
  width: 100%;
  height: 37px;
  margin-top: 3px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  background: #ffffff;
  color: #374151;
  font-size: 13px;
  font-weight: 700;
  cursor: not-allowed;
}
.bookings-section {margin-top: 20px;}
.bookings-section h2 {margin-bottom: 17px;}
.table-container {
  width: 100%;
  overflow-x: auto;
  border: 2px solid #e2e8f0;
  border-radius: 9px;
}
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  white-space: nowrap;
}
thead {background: #f3f4f6;}
th {
  padding: 13px 10px;
  font-size: 12px;
  font-weight: 700;
}
td {
  padding: 12px 10px;
  font-size: 12px;
  border-top: 1px solid #e2e8f0;
}
.booking-status {
  display: inline-block;
  padding: 5px 8px;
  border-radius: 5px;
  font-size: 12px;
}
.booking-status.booked {
  color: #15803d;
  background: #f0fdf4;
}
.booking-status.cancelled {
  color: #dc2626;
  background: #fef2f2;
}
.booking-status.completed {
  color: #155eef;
  background: #eff6ff;
}
.view-button {
  padding: 7px 10px;
  border: 2px solid #8bb5ff;
  border-radius: 6px;
  background: #ffffff;
  color: #155eef;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
.view-button:hover {background: #eff6ff;}
.view-all {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
.view-all span {
  color: #155eef;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
}
.view-all span:hover {text-decoration: underline;}
.message {
  padding: 20px;
  text-align: center;
  font-size: 14px;
}
.error-message {color: #dc2626;}
.error-message button {
  margin-left: 10px;
  padding: 6px 12px;
  border: 1px solid #155eef;
  border-radius: 5px;
  background: #ffffff;
  color: #155eef;
  cursor: pointer;
}
.empty-message {
  padding: 20px;
  text-align: center;
  color: #64748b;
  font-size: 13px;
}
@media (max-width: 900px) {.trek-grid {grid-template-columns: repeat(2, minmax(0, 1fr));}}
@media (max-width: 650px) {
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
  .menu-item span:last-child {display: none;}
  .topbar {padding: 0 12px;}
  .topbar h3 {font-size: 12px;}
  .profile {
    font-size: 12px;
    gap: 5px;
  }
  .dashboard-content {padding: 18px 12px;}
  .section-heading {
    align-items: flex-start;
    flex-direction: column;
  }
  .filters {width: 100%;}
  .filters select {
    flex: 1;
    min-width: 0;
  }
  .trek-grid {grid-template-columns: 1fr;}
  .trek-image {height: 180px;}
}
</style>