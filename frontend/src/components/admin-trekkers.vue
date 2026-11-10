<template>
  <div class="brand">
    <div>
        <h1>Treknologia</h1>
        <h4>Explore the unexplored</h4>
    </div>
    <div style="align-content: center; margin-left: auto; margin-right: 80px; font-weight: 700; font-family: sans-serif; font-size: large;">{{ admin.username }}</div>
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
    <div class="main-section">
      <main class="dashboard-content">
          <div class="page-heading">
            <h1>Trekkers List</h1>
          </div>
          <input class="search-box" v-model="search" type="text" placeholder="Search trekkers..."/>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Contact</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="trekker in trekkers" :key="trekker.id">
                  <td>{{ trekker.id }}</td>
                  <td>{{ trekker.name }}</td>
                  <td>{{ trekker.email }}</td>
                  <td>{{ trekker.contact }}</td>
                  <td><span class="status" :class="trekker.status">{{ trekker.status }}</span></td>
                  <td>
                    <button v-if="trekker.status === 'Active'" class="action-button block-button" @click="changeStatus(trekker)">Blacklist</button>
                    <button v-else class="action-button whitelist-button" @click="changeStatus(trekker)">Whitelist</button>
                  </td>
                </tr>
                <tr v-if="filteredTrekkers.length === 0">
                  <td colspan="6" class="empty-message">No trekkers found.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="notice">
            <span class="notice-icon">ⓘ</span>
            <p>Blacklisted trekkers cannot login or access the system.</p>
          </div>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminManageTrekkers",

  data() {
    return {
      showForm: false,
      search: "",
      activeMenu: "Trekkers",
      error: "",
      menuItems: [
        { name: "Dashboard", icon: "⌂", path: "/admin/dashboard" },
        { name: "Treks", icon: "♧", path: "/admin/treks" },
        { name: "Trekking Staff", icon: "♙", path: "/admin/trekking-staff" },
        { name: "Trekkers", icon: "♙", path: "/admin/trekkers" },
        { name: "Bookings", icon: "♘", path: "/admin/bookings" },
      ],
      trekkers: [],
      admin: {username: "Admin", email: ""}
    };
  },

  computed: {
    filteredTrekkers() {
      const value = this.search.toLowerCase();

      return this.trekkers.filter(trekker =>
        String(trekker.id).toLowerCase().includes(value) ||
        trekker.name.toLowerCase().includes(value) ||
        trekker.email.toLowerCase().includes(value) ||
        trekker.contact.includes(value) ||
        trekker.status.toLowerCase().includes(value)
      );
    }
  },

  mounted() {
    this.fetchTrekkersList();
  },

  methods: {
    async fetchTrekkersList() {
        try {
            const response = await axios.get(
                "http://localhost:5000/api/admin/trekkers",
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`
                    }
                }
            );

            console.log("Trekkers API response:", response.data);

            if (response.data.success) {
                this.admin = response.data.user;
                this.trekkers = response.data.trekkers || [];
            } else {
                this.error = response.data.message || "Failed to load trekkers.";
            }
        } catch (error) {
            console.error(
                "Fetch trekkers error:",
                error.response?.status,
                error.response?.data || error.message
            );

            this.error =
                error.response?.data?.message ||
                "Unable to fetch trekkers.";
        }
    },

    async changeStatus(trekker) {
      const newStatus = trekker.status === "Active" ? "Blacklisted" : "Active";
      try {
        const response = await axios.put(`http://localhost:5000/api/admin/trekkers/${trekker.id}/status`,
          {status: newStatus },
          {headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}}
        );
        if (response.data.success) {
          trekker.status = newStatus;
        }
      } catch (error) {
        console.error("Change status error:", error.response?.data || error);
        this.error = error.response?.data?.message || "Failed to change trekker status.";
      }
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

.btn {
    padding: 5px 10px;
    text-decoration: none;
    border: 2px solid;
    background-color: #af8523;
    color: black;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 4px;
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
    /* padding: 12px 12px; */
}

.topbar {
    height: 55px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 25px;
    border-bottom: 2px solid #e2e8f0;
    background: #ffffff;
}

.topbar h3 {
    margin: 0;
    font-size: 20px;
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
    padding: 22px 18px;
}

.dashboard-content h1 {
    margin: 0 0 22px;
    font-size: 30px;
    font-weight: 700;
}

.page-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;
    margin-bottom: 20px;
}

.page-heading h1 {
    margin: 0;
}

.create-button {
    padding: 11px 17px;
    border: 1px solid #155eef;
    border-radius: 5px;
    background: #155eef;
    color: #ffffff;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

.create-button:hover {
    background: #104bc4;
}

.search-box {
    width: 100%;
    height: 40px;
    margin-bottom: 18px;
    padding: 0 13px;
    border: 2px solid #e2e8f0;
    border-radius: 7px;
    outline: none;
    font-size: 13px;
}

.search-box:focus {
    border-color: #93b4ff;
}

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

thead {
    background: #c5e7ff;
}

th {
    padding: 13px 9px;
    font-size: 15px;
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
    display: inline-block;
    padding: 5px 9px;
    border: 1px solid;
    border-radius: 5px;
    font-size: 12px;
    font-weight: 600;
}

.status.Active {
    border-color: #86d5a8;
    color: #15803d;
    background: #f0fdf4;
}

.status.Blacklisted {
    border-color: #fca5a5;
    color: #dc2626;
    background: #fef2f2;
}

.action-button {
    padding: 6px 9px;
    border: 1px solid;
    border-radius: 5px;
    background: #ffffff;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
}

.block-button {
    border-color: #fca5a5;
    color: #dc2626;
}

.block-button:hover {
    background: #fef2f2;
}

.whitelist-button {
    border-color: #86d5a8;
    color: #15803d;
}

.whitelist-button:hover {
    background: #f0fdf4;
}

.empty-message {
    padding: 25px;
    text-align: center;
    color: #64748b;
}

.notice {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-top: 28px;
    padding: 15px;
    border: 1px solid #b7d0ff;
    border-radius: 7px;
    background: #dfecf3;
}

.notice-icon {
    color: #155eef;
    font-size: 22px;
}

.notice p {
    margin: 0;
    font-size: 13px;
    line-height: 1.5;
}

.staff-form {
    width: 100%;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px 16px;
}

.form-grid input {
    width: 100%;
    height: 39px;
    padding: 0 11px;
    border: 2px solid #e2e8f0;
    border-radius: 7px;
    outline: none;
    font-family: inherit;
    font-size: 13px;
}

.form-grid input:focus {
    border-color: #93b4ff;
}

.form-grid input::placeholder {
    color: #64748b;
}

.form-grid .full-width {
    grid-column: 1 / -1;
}

.status-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    gap: 16px;
    margin-top: 10px;
}

.status-row label {
    font-size: 13px;
    font-weight: 600;
}

.status-row select {
    width: 100%;
    height: 39px;
    padding: 0 10px;
    border: 2px solid #e2e8f0;
    border-radius: 7px;
    background: #ffffff;
    font-family: inherit;
    font-size: 13px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    margin-top: 12px;
}

.cancel-button {
    padding: 10px 22px;
    border: 2px solid #d5dce5;
    border-radius: 5px;
    background: #ffffff;
    color: #111827;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
}

.cancel-button:hover {
    background: #f8fafc;
}

.form-error {
    margin: 12px 0 0;
    color: #dc2626;
    font-size: 13px;
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

    .dashboard-content {
        padding: 18px 12px;
    }

    .page-heading {
        align-items: flex-start;
        flex-direction: column;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

    .form-grid .full-width {
        grid-column: 1;
    }

    .status-row {
        grid-template-columns: 1fr;
        gap: 7px;
    }

    .notice {
        align-items: flex-start;
    }
}
</style>