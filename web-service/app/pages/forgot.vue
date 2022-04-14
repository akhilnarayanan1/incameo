<template>
  <div class="forgot flex items-center justify-center h-screen">
    <div class="card shadow max-w-sm m-4">
      <div class="card-body">
          
        <div class="text-4xl font-bold mb-4">Forgot Password</div>
        <div class="mb-4">Enter the e-mail associated with your account</div>

        <form @submit.prevent="forgotPassword">
          <div class="form-control">
            <div class="input-group border rounded-lg">
              <span class="bg-transparent">📧</span>
              <input v-model="forgot_email" type="email" placeholder="Enter your e-mail" class="w-full input"> 
            </div>  
              <InputLabel labelName="forgot_email" />
          </div> 
          
          <button type="submit" :class="loading.forgot ? 
          'btn btn-block glass bg-primary hover:bg-primary loading': 
          'btn btn-block glass bg-primary hover:bg-primary'">
            FORGOT PASSWORD
          </button>
        </form>

      </div>
    </div> 

  </div>
</template>

<script setup lang="ts">

  let loading: { forgot: boolean } = reactive({ forgot: false });

  const forgot_email = ref("");

  const forgotPassword = () => {

  };
</script>