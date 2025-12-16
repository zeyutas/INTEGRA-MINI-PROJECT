<template>
  <div class="profile-page" v-loading="loading">
    <div class="profile-top">
      <div>
        <p class="eyebrow">Profile</p>
        <h2>Welcome back, {{ fullName }}</h2>
        <p class="muted">Data is loaded from the live API. Editable fields are highlighted below.</p>
      </div>
      <el-button type="text" @click="handleLogout">Logout</el-button>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :md="8">
        <el-card class="summary-card" shadow="hover">
          <div class="avatar-row">
            <avatar-display :src="form.avatar_url || profile.avatar_url" :name="fullName" :size="110">
              <strong>{{ fullName }}</strong>
              <span class="muted">{{ profile.role || 'Advisor' }}</span>
            </avatar-display>
          </div>
          <div class="tags-row">
            <el-tag type="info" v-if="profile.advisor_id">{{ profile.advisor_id }}</el-tag>
            <el-tag type="success" v-if="profile.role">{{ profile.role }}</el-tag>
          </div>
          <el-descriptions :column="1" size="small" class="profile-descriptions">
            <el-descriptions-item label="Username">{{ profile.username || '—' }}</el-descriptions-item>
            <el-descriptions-item label="Email">{{ profile.email || '—' }}</el-descriptions-item>
            <el-descriptions-item label="Firm">{{ profile.firm_name || '—' }}</el-descriptions-item>
            <el-descriptions-item label="Date joined">{{ formattedDateJoined }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="16">
        <el-card shadow="hover">
          <div class="card-heading">
            <div>
              <p class="eyebrow">Editable</p>
              <h3>Profile details</h3>
            </div>
            <el-tag type="success" effect="plain">Live API</el-tag>
          </div>

          <el-form label-position="top" @submit.native.prevent="onSave">
            <el-row :gutter="12">
              <el-col :span="12">
                <base-input
                  v-model="form.first_name"
                  label="First name"
                  placeholder="Kelly"
                  :error="errors.first_name"
                  clearable
                />
              </el-col>
              <el-col :span="12">
                <base-input
                  v-model="form.last_name"
                  label="Last name"
                  placeholder="Li"
                  :error="errors.last_name"
                  clearable
                />
              </el-col>
            </el-row>

            <base-input
              v-model="form.avatar_url"
              label="Avatar URL"
              placeholder="https://..."
              :error="errors.avatar_url"
              clearable
            />

            <base-input
              v-model="form.bio"
              type="textarea"
              :rows="4"
              label="Bio"
              placeholder="Tell clients about your focus areas and style."
              :error="errors.bio"
            />

            <el-divider>Read-only</el-divider>

            <el-row :gutter="12">
              <el-col :span="12">
                <base-input :value="profile.username" label="Username" disabled />
              </el-col>
              <el-col :span="12">
                <base-input :value="profile.email" label="Email" disabled />
              </el-col>
            </el-row>

            <el-row :gutter="12">
              <el-col :span="12">
                <base-input :value="profile.advisor_id" label="Advisor ID" disabled />
              </el-col>
              <el-col :span="12">
                <base-input :value="profile.firm_name" label="Firm" disabled />
              </el-col>
            </el-row>

            <el-row :gutter="12">
              <el-col :span="12">
                <base-input :value="profile.role" label="Role" disabled />
              </el-col>
              <el-col :span="12">
                <base-input :value="formattedDateJoined" label="Date joined" disabled />
              </el-col>
            </el-row>

            <div class="form-actions">
              <el-button type="primary" :loading="saving" @click="onSave">Save changes</el-button>
              <span class="muted">Saves via PATCH /user/profile/</span>
            </div>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import AvatarDisplay from '../components/AvatarDisplay.vue';
import BaseInput from '../components/BaseInput.vue';
import { logout } from '../services/auth';
import { getProfile, updateProfile } from '../services/profile';

export default {
  name: 'Profile',
  components: { AvatarDisplay, BaseInput },
  data() {
    return {
      profile: {
        avatar_url: '',
        role: '',
        firm_name: '',
        advisor_id: '',
        username: '',
        email: '',
        date_joined: '',
        first_name: '',
        last_name: '',
        bio: ''
      },
      form: {
        first_name: '',
        last_name: '',
        bio: '',
        avatar_url: ''
      },
      errors: {},
      loading: true,
      saving: false
    };
  },
  computed: {
    fullName() {
      const firstName = this.form.first_name || this.profile.first_name;
      const lastName = this.form.last_name || this.profile.last_name;
      return [firstName, lastName].filter(Boolean).join(' ') || 'Advisor';
    },
    formattedDateJoined() {
      if (!this.profile.date_joined) return '—';
      const date = new Date(this.profile.date_joined);
      return Number.isNaN(date.getTime()) ? this.profile.date_joined : date.toLocaleString();
    }
  },
  created() {
    this.loadProfile();
  },
  methods: {
    async loadProfile() {
      this.loading = true;
      try {
        const data = await getProfile();
        this.profile = data;
        this.form = {
          first_name: data.first_name || '',
          last_name: data.last_name || '',
          bio: data.bio || '',
          avatar_url: data.avatar_url || ''
        };
      } catch (error) {
        if (error?.response?.status === 401) {
          this.$message.error('登录已过期，请重新登录');
          this.handleLogout();
        } else {
          this.$message.error('Failed to load profile data');
        }
      } finally {
        this.loading = false;
      }
    },
    validate() {
      const errors = {};
      if (!this.form.first_name) errors.first_name = 'First name is required.';
      if (!this.form.last_name) errors.last_name = 'Last name is required.';
      if (this.form.bio && this.form.bio.length > 1024) {
        errors.bio = 'Bio should be under 1024 characters.';
      }
      if (this.form.avatar_url && !/^https?:\/\//i.test(this.form.avatar_url)) {
        errors.avatar_url = 'Avatar URL should start with http(s)://';
      }
      this.errors = errors;
      return Object.keys(errors).length === 0;
    },
    async onSave() {
      if (!this.validate()) return;
      this.saving = true;
      try {
        const updated = await updateProfile(this.form);
        this.profile = { ...this.profile, ...updated };
        this.form = {
          first_name: updated.first_name || '',
          last_name: updated.last_name || '',
          bio: updated.bio || '',
          avatar_url: updated.avatar_url || ''
        };
        console.log('Updated profile data:', updated);
        this.$message.success('Profile saved');
      } catch (error) {
        if (error?.response?.status === 401) {
          this.$message.error('登录已过期，请重新登录');
          this.handleLogout();
        } else {
          const msg = error?.response?.data?.detail || 'Unable to save profile';
          this.$message.error(msg);
        }
      } finally {
        this.saving = false;
      }
    },
    handleLogout() {
      logout();
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 11px;
  color: #7a8499;
}

.profile-top h2 {
  margin: 6px 0 4px;
}

.muted {
  color: #7a8499;
  font-size: 13px;
}

.summary-card {
  min-height: 100%;
}

.avatar-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.tags-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.profile-descriptions {
  margin-top: 8px;
}

.card-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.form-actions {
  margin-top: 8px;
  display: flex;
  gap: 12px;
  align-items: center;
}

@media (max-width: 768px) {
  .profile-top {
    flex-direction: column;
  }

  .avatar-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
