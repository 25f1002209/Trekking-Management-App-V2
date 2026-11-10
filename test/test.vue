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
        const response = await axios.get("http://localhost:5000/api/trekker/dashboard", { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
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