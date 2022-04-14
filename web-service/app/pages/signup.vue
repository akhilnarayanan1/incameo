<template>
  <div class="flex items-center justify-center h-screen">
    <div class="card shadow max-w-sm m-4">
      <div class="card-body">
        <div class="text-4xl font-bold mb-4">Signup</div>
        <div class="mb-4">Already have an account? <NuxtLink to="/login" class="text-primary font-bold" replace>Login here</NuxtLink>, and stay ahead!</div>

        <form @submit.prevent="createAccount">
          
          <div class="form-control">
            <div class="input-group border rounded-lg">
              <span class="bg-transparent">📧</span>
              <input v-model="signup_email" type="email" placeholder="Enter your e-mail" class="w-full input"> 
            </div>  
            <InputLabel labelName="signup_email"></InputLabel>
          </div> 
          
          <div class="form-control">
            <div class="input-group border rounded-lg">
              <span class="bg-transparent">🔒</span>
              <input v-model="signup_password" type="password" placeholder="Choose a password" class="w-full input" autocomplete="false"> 
            </div>  
            <InputLabel labelName="signup_password"/>
          </div> 
          <div class="form-control">
            <div class="input-group border rounded-lg">
              <span class="bg-transparent">🔒</span>
              <input v-model="signup_confirm_password" type="password" placeholder="Confirm your password" class="w-full input" autocomplete="false"> 
            </div>  
            <InputLabel labelName="signup_confirm_password"/>
          </div> 
          <!-- <div class="form-control">
              <div class="label">
                  <input type="checkbox" checked="checked" class="checkbox checkbox-primary">
                  <span class="label-text m-4">I agree to <NuxtLink to="/terms" class="text-primary">Terms of use</NuxtLink> & <NuxtLink to="/privacy" class="text-primary">Privacy Policy</NuxtLink></span> 
              </div>   
          </div> -->

          <button type="submit" :class="loading.signup ? 
          'btn btn-block glass bg-primary hover:bg-primary loading': 
          'btn btn-block glass bg-primary hover:bg-primary'">
            CREATE ACCOUNT
          </button>
        </form>
      </div>
    </div> 
  </div>
</template>

<script setup lang="ts">
  
  let loading: { signup: boolean } = reactive({ signup: false });

  const signup_email = ref("");
  const signup_password = ref("");
  const signup_confirm_password = ref("");

  const createAccount = () => {

  };
</script>