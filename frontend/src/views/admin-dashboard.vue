<template>
  <div class="dashboard">

    <aside class="sidebar">
      <div class="menu-icon" @click="toggleSidebar">☰</div>

      <div class="sidebar-menu">
        <div
          v-for="item in menuItems"
          :key="item.name"
          class="menu-item"
          :class="{ active: activeMenu === item.name }"
          @click="selectMenu(item)"
        >
          <span class="menu-symbol">{{ item.icon }}</span>
          <span>{{ item.name }}</span>
        </div>
      </div>
    </aside>

    <div class="main-section" :class="{ expanded: sidebarHidden }">

      <header class="topbar">
        <h3>Trekking Management Application</h3>

        <div class="admin-profile">
          <span class="profile-icon">♙</span>
          <span>Admin</span>
          <span>⌄</span>
        </div>
      </header>

      <main class="dashboard-content">
        <h1>Dashboard {{ user.username }}</h1>

        <div class="stats-container">
          <div class="stat-card">
            <div>
              <h3>Total Treks</h3>
              <p>{{ totalTreks }}</p>
            </div>
            <span class="stat-icon">♧</span>
          </div>

          <div class="stat-card">
            <div>
              <h3>Total Users<br>(Trekkers)</h3>
              <p>{{ totalTrekkers }}</p>
            </div>
            <span class="stat-icon">♙</span>
          </div>

          <div class="stat-card">
            <div>
              <h3>Total Trekking Staff</h3>
              <p>{{ totalStaffs }}</p>
            </div>
            <span class="stat-icon">♙</span>
          </div>

          <div class="stat-card">
            <div>
              <h3>Total Bookings</h3>
              <p>{{ totalBookings }}</p>
            </div>
            <span class="stat-icon">▦</span>
          </div>
        </div>

        <section class="bookings-section">
          <h2>Recent Bookings</h2>

          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Booking ID</th>
                  <th>User (Trekker)</th>
                  <th>Trek</th>
                  <th>Booking Date</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="booking in bookings" :key="booking.id">
                  <td>{{ booking.id }}</td>
                  <td>{{ booking.user }}</td>
                  <td>{{ booking.trek }}</td>
                  <td>{{ booking.date }}</td>
                  <td>
                    <span
                      class="status"
                      :class="booking.status.toLowerCase()"
                    >
                      {{ booking.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="view-all">
            <button @click="viewAllBookings">
              View All Bookings <span>→</span>
            </button>
          </div>
        </section>
      </main>

    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminDashboard",

  data() {
    return {
      sidebarHidden: false,
      activeMenu: "Dashboard",
      user: {},
      totalTreks: 0,
      totalUsers: 0,
      totalStaff: 0,
      totalBookings: 0,

      menuItems: [
        { name: "Dashboard", icon: "⌂", path: "/admin-dashboard" },
        { name: "Treks", icon: "♧", path: "/admin-treks" },
        { name: "Trekking Staff", icon: "♙", path: "/admin/trekking-staff" },
        { name: "Users (Trekkers)", icon: "♙", path: "/admin-users" },
        { name: "Bookings", icon: "▦", path: "/admin-bookings" },
        { name: "Search", icon: "⌕", path: "/admin-search" },
        { name: "Reports", icon: "▤", path: "/admin-reports" },
        { name: "Settings", icon: "⚙", path: "/admin-settings" },
        { name: "Logout", icon: "⇥", path: "/" }
      ],

      bookings: []
    };
  },

  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get("http://localhost:5000/api/admin-dashboard", {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
        });
        const data = response.data;

        if (data.success) {
            this.user = data.user;
            this.totalTreks = data.total_treks;
            this.totalTrekkers = data.total_trekkers;
            this.totalStaffs = data.total_staffs;
            this.totalBookings = data.total_bookings;
            this.bookings = data.bookings;
        } else {
          console.error("Failed to fetch dashboard data:", data.message);
        }
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },

    toggleSidebar() {
      this.sidebarHidden = !this.sidebarHidden;
    },

    selectMenu(item) {
      this.activeMenu = item.name;

      if (item.name === "Logout") {
        this.$router.push("/");
      } else if (item.path !== this.$route.path) {
        this.$router.push(item.path);
      }
    },

    viewAllBookings() {
      this.$router.push("/admin-bookings");
    }
  }
};
</script>

<style scoped>
* {
    box-sizing: border-box;
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
    width: 205px;
    min-width: 205px;
    min-height: 100vh;
    border-right: 2px solid #e2e8f0;
    background: #ffffff;
    transition: width 0.2s ease;
}

.menu-icon {
    height: 65px;
    display: flex;
    align-items: center;
    padding: 0 25px;
    border-bottom: 2px solid #e2e8f0;
    font-size: 25px;
    cursor: pointer;
}

.sidebar-menu {
    padding: 14px 5px;
}

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
    transition: background 0.2s ease;
}

.menu-item:hover {
    background: #f1f5f9;
}

.menu-item.active {
    color: #155eef;
    background: #e8f0ff;
}

.menu-symbol {
    width: 23px;
    text-align: center;
    font-size: 22px;
    flex-shrink: 0;
}

.main-section {
    flex: 1;
    min-width: 0;
}

.main-section.expanded {
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

.admin-profile {
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
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 25px;
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
    margin: 0 0 18px;
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

.bookings-section h2 {
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
    background: #f3f4f6;
}

th {
    padding: 16px 14px;
    font-size: 14px;
    font-weight: 700;
}

td {
    padding: 17px 14px;
    font-size: 15px;
    border-top: 1px solid #e2e8f0;
}

tbody tr:hover {
    background: #f8fafc;
}

.status {
    font-weight: 600;
}

.status.booked {
    color: #15803d;
}

.status.cancelled {
    color: #dc2626;
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

    .menu-symbol {
        font-size: 21px;
    }

    .topbar {
        padding: 0 12px;
    }

    .topbar h3 {
        font-size: 13px;
    }

    .admin-profile {
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
        min-height: 110px;
    }

    .bookings-section h2 {
        font-size: 19px;
    }

    th,
    td {
        padding: 13px 10px;
    }
}
</style>