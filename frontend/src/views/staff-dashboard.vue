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

        <div class="staff-profile">
          <span class="profile-icon">♙</span>
          <span>{{ user.username || "Trekking Staff" }}</span>
          <span>⌄</span>
        </div>
      </header>

      <main class="dashboard-content">
        <h1>My Dashboard</h1>

        <div v-if="loading" class="message">
          Loading dashboard...
        </div>

        <div v-else-if="error" class="error-message">
          {{ error }}
          <button @click="fetchDashboardData">Retry</button>
        </div>

        <template v-else>
          <div class="stats-container">

            <div class="stat-card">
              <div>
                <h3>Assigned Treks</h3>
                <p>{{ assignedTreks }}</p>
              </div>
              <span class="stat-icon">▦</span>
            </div>

            <div class="stat-card">
              <div>
                <h3>Total Participants</h3>
                <p>{{ totalParticipants }}</p>
              </div>
              <span class="stat-icon">♙</span>
            </div>

            <div class="stat-card">
              <div>
                <h3>Ongoing Treks</h3>
                <p>{{ ongoingTreks }}</p>
              </div>
              <span class="stat-icon">♧</span>
            </div>

          </div>

          <section class="treks-section">
            <h2>My Assigned Treks</h2>

            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Trek Name</th>
                    <th>Dates</th>
                    <th>Participants</th>
                    <th>Slots</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  <tr v-for="trek in treks" :key="trek.id">
                    <td>{{ trek.name }}</td>
                    <td>{{ trek.dates }}</td>
                    <td>{{ trek.participants }}</td>
                    <td>{{ trek.slots }}</td>
                    <td>
                      <span
                        class="status"
                        :class="trek.status.toLowerCase()"
                      >
                        {{ trek.status }}
                      </span>
                    </td>
                    <td>
                      <button
                        class="action-button"
                        @click="manageTrek(trek)"
                      >
                        {{ trek.status === "Closed" ? "View" : "Manage" }}
                      </button>
                    </td>
                  </tr>

                  <tr v-if="treks.length === 0">
                    <td colspan="6" class="empty-message">
                      No assigned treks found.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </template>

      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "StaffDashboard",

  data() {
    return {
      sidebarHidden: false,
      activeMenu: "Dashboard",
      loading: false,
      error: "",

      user: {
        username: ""
      },

      assignedTreks: 0,
      totalParticipants: 0,
      ongoingTreks: 0,

      treks: [],

      menuItems: [
        { name: "Dashboard", icon: "⌂", path: "/staff-dashboard" },
        { name: "My Treks", icon: "♧", path: "/staff-treks" },
        { name: "Participants", icon: "♙", path: "/staff-participants" },
        { name: "Profile", icon: "♙", path: "/staff-profile" },
        { name: "Logout", icon: "⇥", path: "/" }
      ]
    };
  },

  mounted() {
    this.fetchDashboardData();
  },

  methods: {
    async fetchDashboardData() {
      this.loading = true;
      this.error = "";

      try {
        const response = await axios.get(
          "http://localhost:5000/api/staff-dashboard",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`
            }
          }
        );

        const data = response.data;

        if (data.success) {
          this.user = data.user || { username: "" };
          this.assignedTreks = data.assigned_treks;
          this.totalParticipants = data.total_participants;
          this.ongoingTreks = data.ongoing_treks;
          this.treks = data.treks || [];
        } else {
          this.error = data.message || "Unable to load dashboard.";
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.error = "Your session has expired. Please log in again.";
        } else {
          this.error =
            error.response?.data?.message ||
            "Unable to load dashboard. Check your backend.";
        }

        console.error("Dashboard error:", error);
      } finally {
        this.loading = false;
      }
    },

    toggleSidebar() {
      this.sidebarHidden = !this.sidebarHidden;
    },

    selectMenu(item) {
      this.activeMenu = item.name;

      if (item.name === "Logout") {
        localStorage.removeItem("token");
        this.$router.push("/");
      } else if (item.path !== this.$route.path) {
        this.$router.push(item.path);
      }
    },

    manageTrek(trek) {
      this.$router.push({
        path: "/staff-manage-trek",
        query: { id: trek.id }
      });
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

.staff-profile {
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
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 35px;
}

.stat-card {
    min-height: 100px;
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
    font-size: 14px;
    line-height: 1.4;
    font-weight: 700;
}

.stat-card p {
    margin: 0;
    font-size: 30px;
    font-weight: 700;
}

.stat-icon {
    font-size: 32px;
    color: #111827;
}

.treks-section h2 {
    margin: 0 0 18px;
    font-size: 20px;
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
    padding: 13px 10px;
    font-size: 13px;
    font-weight: 700;
}

td {
    padding: 14px 10px;
    font-size: 13px;
    border-top: 1px solid #e2e8f0;
}

tbody tr:hover {
    background: #f8fafc;
}

.status {
    font-weight: 600;
}

.status.open {
    color: #15803d;
}

.status.closed {
    color: #dc2626;
}

.action-button {
    padding: 8px 13px;
    border: 1px solid #93b4ff;
    border-radius: 5px;
    background: #ffffff;
    color: #155eef;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

.action-button:hover {
    background: #e8f0ff;
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

.error-message button {
    margin-left: 12px;
    padding: 6px 12px;
    border: 1px solid #b91c1c;
    border-radius: 5px;
    background: #ffffff;
    color: #b91c1c;
    cursor: pointer;
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
        font-size: 18px;
    }

    th,
    td {
        padding: 12px 8px;
    }
}
</style>