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
        <div class="menu-item" style="margin-top: 370px;" @click="logout"><span class="menu-symbol">⇥</span><span>Logout</span></div>
      </div>
    </aside>
    <div class="main-section">
      <main class="dashboard-content">
        <template v-if="!isManage">
          <div class="page-heading">
            <h1>My Treks</h1>
          </div>
          <input class="search-box" v-model="search" type="text" placeholder="Search treks..."/>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Trek Name</th>
                  <th>Location</th>
                  <th>Duration</th>
                  <th>Participants</th>
                  <th>Available Slots</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="trek in treks" :key="trek.id">
                  <td>{{ trek.id }}</td>
                  <td>{{ trek.name }}</td>
                  <td>{{ trek.location }}</td>
                  <td>{{ trek.start_date }} to {{ trek.end_date }}</td>
                  <td>{{ trek.participants }}</td>
                  <td>{{ trek.available_slots }}</td>
                  <td><span class="status" :class="trek.status">{{ trek.status }}</span></td>
                  <td><button class="action-button block-button" style="color: blue; border-color: blue; font-weight: bold;" @click="openManage(trek)">Manage</button></td>
                </tr>
                <tr v-if="filteredTreks.length === 0">
                  <td colspan="8" class="empty-message">No treks found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
        <template v-else>
            <h1>Manage Trek</h1>
            <form class="staff-form" @submit.prevent="updateTrek(selectedTrek.id)">
                <div class="form-grid">
                    <input v-model="form.name" type="text" placeholder="Trek Name" readonly/>
                    <input v-model="form.location" type="text" placeholder="Location" readonly/>
                    <input v-model="form.difficulty" type="text" placeholder="Difficulty Level" readonly/>
                    <input v-model="form.price" type="number" placeholder="Price" readonly/>
                    <input v-model="form.description" type="text" placeholder="Description" readonly/>
                    <input v-model="form.photo" type="text" placeholder="Photo URL" readonly/>
                    <input v-model="form.availableSlots" type="number" placeholder="Available Slots" required/>
                    <span style="font-size: medium; font-weight: 600; padding: 5px;"></span>
                    <label style="font-size: large; font-weight: 600; padding: 10px 15px;" for="start-date">Start Date</label>
                    <input v-model="form.start_date" type="date" placeholder="Start Date" readonly/>
                    <label style="font-size: large; font-weight: 600; padding: 10px 15px;" for="end-date">End Date</label>
                    <input v-model="form.end_date" type="date" placeholder="End Date" readonly/>
                </div>
                <div class="status-row">
                    <label style="font-size: large; font-weight: 600; padding: 10px 15px;" for="staff-status">Status</label>
                    <select id="staff-status" v-model="form.status">
                        <option>Open</option>
                        <option>Upcoming</option>
                        <option>Closed</option>
                    </select>
                </div>
                <p v-if="error" class="form-error">{{ error }}</p>
                <div class="form-actions">
                    <button type="button" class="cancel-button" @click="closeManage">Close</button>
                    <button type="submit" class="create-button">Update Trek</button>
                </div>
            </form>
            <div class="notice">
                <span class="notice-icon">ⓘ</span>
                <p>You can manage the trek details here.</p>
            </div>
        </template>
      </main>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "StaffManageTreks",

  data() {
    return {
      selectedTrek: null,
      isManage: false,
      search: "",
      activeMenu: "Treks",
      error: "",
      menuItems: [
        { name: "Dashboard", icon: "⌂", path: "/staff/dashboard" },
        { name: "Treks", icon: "♧", path: "/staff/treks" },
        { name: "Participants", icon: "♙", path: "/staff/participants" },
        { name: "Profile", icon: "♙", path: "/staff/profile" }
      ],
      form: {name: "", location: "", description: "", start_date: "", end_date: "", difficulty: "", price: "", photo: "", availableSlots: "", status: "Open"},
      treks: [],
      user: {name: ""}
    };
  },

  computed: {
    filteredTreks() {
      const value = this.search.toLowerCase();

      return this.treks.filter(trek =>
        String(trek.id).toLowerCase().includes(value) ||
        trek.name.toLowerCase().includes(value) ||
        trek.location.toLowerCase().includes(value) ||
        trek.difficulty.toLowerCase().includes(value) ||
        trek.status.toLowerCase().includes(value)
      );
    }
  },

  mounted() {
    this.fetchTreksList();
  },

  methods: {
    async fetchTreksList() {
        try {
            const response = await axios.get("http://localhost:5000/api/staff/treks",
                {headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}}
            );
            console.log("Treks API response:", response.data);
            if (response.data.success) {
                this.user = response.data.user;
                this.treks = response.data.treks || [];
            } else {
                this.error = response.data.message || "Failed to load treks.";
            }
        } catch (error) {
            console.error("Fetch treks error:", error.response?.status, error.response?.data || error.message);
            this.error = error.response?.data?.message || "Unable to fetch treks.";
        }
    },

    openManage(trek) {
      this.isManage = true;
      this.showForm = true;
      this.selectedTrek = trek;
      this.form = {
        name: trek.name,
        location: trek.location,
        description: trek.description,
        start_date: trek.start_date ? trek.start_date.split("T")[0] : "",
        end_date: trek.end_date ? trek.end_date.split("T")[0] : "",
        difficulty: trek.difficulty,
        price: trek.price,
        photo: trek.photo,
        availableSlots: trek.available_slots,
        status: trek.status,
        assignedStaffs: (trek.assigned_staffs || []).map(id => typeof id === "object" ? Number(id.id) : Number(id))
      };
    },

    closeManage() {
      this.isManage = false;
      this.showForm = false;
      this.error = "";
      this.form = {
        name: "",
        location: "",
        description: "",
        start_date: "",
        end_date: "",
        difficulty: "",
        price: "",
        photo: "",
        availableSlots: "",
        status: "Open",
      };
    },

    async updateTrek(id) {
        this.error = "";
        try {
            const response = await axios.post(
                `http://localhost:5000/api/staff/treks/${id}/manage`,
                {
                    name: this.form.name,
                    location: this.form.location,
                    description: this.form.description,
                    start_date: this.form.start_date,
                    end_date: this.form.end_date,
                    difficulty: this.form.difficulty,
                    price: this.form.price,
                    photo: this.form.photo,
                    availableSlots: this.form.availableSlots,
                    status: this.form.status,
                    assignedStaffs: this.form.assignedStaffs
                },
                {headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}}
            );

            if (response.data.success) {
                alert("Trek updated successfully!");
                this.closeManage();
                await this.fetchTreksList();
            }
        } catch (error) {
            console.error("Update trek error:", error.response?.data || error);
            this.error = error.response?.data?.message || "Failed to update trek.";
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
    font-size: 16px;
    font-weight: 700;
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

.status.Open {
    border-color: #86d5a8;
    color: #15803d;
    background: #f0fdf4;
}

.status.Closed {
    border-color: #fca5a5;
    color: #dc2626;
    background: #fef2f2;
}
.status.Upcoming {
    border-color: #facc15;
    color: #b45309;
    background: #fffbeb;
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
    background: #f4f7ff;
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
.staff-dropdown {
    position: relative;
    width: 100%;
}

.dropdown-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 12px;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    background: white;
    cursor: pointer;
    font-size: 14px;
}

.dropdown-header:hover {
    border-color: #2563eb;
}

.dropdown-options {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    max-height: 200px;
    overflow-y: auto;
    margin-top: 5px;
    background: white;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    z-index: 100;
}

.staff-option {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 12px;
    cursor: pointer;
    font-size: 13px;
}

.staff-option:hover {
    background: #eff6ff;
}

.staff-option input {
    width: 16px;
    height: 16px;
    accent-color: #155eef;
    cursor: pointer;
}

.staff-option small {
    margin-left: auto;
    color: #64748b;
}

.no-staff {
    padding: 12px;
    text-align: center;
    color: #64748b;
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