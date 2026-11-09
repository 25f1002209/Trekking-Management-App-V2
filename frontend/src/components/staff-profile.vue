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
        <main class="main-section">
            <div class="dashboard-content">
                <h1>My Profile</h1>
                <p>View and manage your personal information and account details.</p>
                <div v-if="error" class="notice">
                    <span class="notice-icon">⚠️</span>
                    <p>{{ error }}</p>
                </div>
                <div v-if="loading" class="empty-message">Loading profile...</div>
                <div v-else>
                    <form class="staff-form" @submit.prevent="updateProfile">
                        <div class="form-grid">
                            <label>Staff ID<input type="text" :value="user.id" disabled/></label>
                            <label>Full Name<input v-model="user.name" type="text" disabled placeholder="Full Name"/></label>
                            <label>Username<input v-model="user.username" type="text" disabled placeholder="Username"/></label>
                            <label>Email Address<input v-model="user.email" type="email" disabled placeholder="Email Address"/></label>
                            <label>Contact Number<input v-model="form.contact" type="text" :disabled="!isEditing" placeholder="Contact Number"/></label>
                            <label>Experience<input v-model="form.experience" type="text" :disabled="!isEditing" placeholder="Experience"/></label>

                            <label class="full-width">
                                Specialization
                                <input v-model="form.specialization" type="text" :disabled="!isEditing" placeholder="Specialization"/>
                            </label>

                            <label class="full-width">
                                Account Status
                                <input type="text" :value="user.status" disabled/>
                            </label>
                        </div>

                        <p v-if="success" style="color: green; margin-top: 12px;">{{ success }}</p>
                        <p v-if="error" class="form-error">{{ error }}</p>

                        <div class="form-actions">
                            <template v-if="!isEditing">
                                <button class="create-button" @click="startEditing">Edit Profile</button>
                            </template>

                            <template v-else>
                                <button class="cancel-button" @click="cancelEditing">Cancel</button>
                                <button type="submit" class="create-button" :disabled="saving">
                                    {{ saving ? 'Saving...' : 'Save Changes' }}
                                </button>
                            </template>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    </div>
</template>
<script>
import axios from "axios";
export default {
    name: "StaffProfile",
    data() {
        return {
            user: {name: ""},
            menuItems: [
                { name: "Dashboard", icon: "⌂", path: "/staff/dashboard" },
                { name: "Treks", icon: "♧", path: "/staff/treks" },
                { name: "Participants", icon: "♙", path: "/staff/participants" },
                { name: "Profile", icon: "♙", path: "/staff/profile" }
            ],
            activeMenu: "Profile",
            profile: {},
            form: {
                contact: "",
                experience: "",
                specialization: ""
            },
            isEditing: false,
            loading: false,
            saving: false,
            error: "",
            success: ""
        };
    },
    mounted() {
        this.fetchProfile();
    },
    methods: {
        async fetchProfile() {
            this.loading = true;
            try {
                const response = await axios.get("http://localhost:5000/api/staff/profile",
                    {headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}}
                );
                if (response.data.success) {
                    this.user = response.data.user;
                    this.form = {
                        contact: this.user.contact || "",
                        experience: this.user.experience || "",
                        specialization: this.user.specialization || ""
                    };
                } else {
                    this.error = response.data.message || "Failed to load profile.";
                }
            } catch (error) {
                console.error("Fetch profile error:", error.response?.data || error);
                this.error = error.response?.data?.message || "Unable to fetch profile.";
            } finally {
                this.loading = false;
            }
        },
        startEditing() {
            this.success = "";
            this.error = "";
            this.isEditing = true;
            this.form = {
                contact: this.user.contact || "",
                experience: this.user.experience || "",
                specialization: this.user.specialization || ""
            };
        },
        cancelEditing() {
            this.isEditing = false;
            this.error = "";
            this.form = {
                contact: this.user.contact || "",
                experience: this.user.experience || "",
                specialization: this.user.specialization || ""
            };
        },
        async updateProfile() {
            this.error = "";
            this.success = "";
            console.log("Form data before validation:", this.form);
            if (!this.form.contact.trim() || !this.form.experience.trim() || !this.form.specialization.trim()) {
                this.error = "Contact, experience and specialization are required.";
                return;
            }
            this.saving = true;
            try {
                const response = await axios.put("http://localhost:5000/api/staff/profile", this.form,
                    {headers: {Authorization: `Bearer ${localStorage.getItem("token")}`}}
                );
                if (response.data.success) {
                    this.user = response.data.user;
                    this.isEditing = false;
                    this.success = "Profile updated successfully.";
                } else {
                    this.error = response.data.message || "Failed to update profile.";
                }
            } catch (error) {
                console.error("Update profile error:", error.response?.data || error);
                this.error = error.response?.data?.message || "Unable to update profile.";
            } finally {
                this.saving = false;
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
}
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
.sidebar-menu {padding: 10px 5px;}
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
.dashboard-content {padding: 22px 18px;}
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
.page-heading h1 {margin: 0;}
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
.create-button:hover {background: #104bc4;}
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
.search-box:focus {border-color: #93b4ff;}
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
thead {background: #c5e7ff;}
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
tbody tr:hover {background: #f8fafc;}
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
.block-button:hover {background: #fef2f2;}
.whitelist-button {
    border-color: #86d5a8;
    color: #15803d;
}
.whitelist-button:hover {background: #f0fdf4;}
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
.staff-form {width: 100%;}
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
    background: #d6e9f1;
}
.form-grid input:focus {border-color: #93b4ff;}
.form-grid input::placeholder {color: #64748b;}
.form-grid .full-width {grid-column: 1 / -1;}
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
.dropdown-header:hover {border-color: #2563eb;}
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
.staff-option:hover {background: #eff6ff;}
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
    .sidebar {width: 65px; min-width: 65px;}
    .menu-icon {justify-content: center; padding: 0;}
    .menu-item {justify-content: center; padding: 12px 5px;}
    .menu-item span:last-child {display: none;}
    .topbar {padding: 0 12px;}
    .topbar h3 {font-size: 13px;}
    .dashboard-content {padding: 18px 12px;}
    .page-heading {align-items: flex-start; flex-direction: column;}
    .form-grid {grid-template-columns: 1fr;}
    .form-grid .full-width {grid-column: 1;}
    .status-row {grid-template-columns: 1fr; gap: 7px;}
    .notice {align-items: flex-start;}
}
</style>