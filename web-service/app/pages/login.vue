<template>
<div class="login flex items-center justify-center h-screen">
    <div class="card shadow max-w-sm m-4">
      <div class="card-body">
          
        <div class="text-4xl font-bold mb-4">Login</div>
        <div class="mb-4">Don't have an account?  <NuxtLink to="/signup" class="text-primary font-bold" replace>Create your account</NuxtLink>, it takes less than a minute</div>

        <form @submit.prevent="loginAccount">
        <div class="form-control">
          <div class="input-group border rounded-lg">
            <span class="bg-transparent">📧</span>
            <input v-model="login_email" type="email" placeholder="Enter your e-mail" class="w-full input">
          </div>  
          <InputLabel labelName="login_email"/>
        </div> 
        
        <div class="form-control">
          <div class="input-group border rounded-lg">
            <span class="bg-transparent">🔒</span>
            <input autocomplete="false" v-model="login_password" type="password" placeholder="Enter password" class="w-full input"> 
          </div>  
          <InputLabel labelName="login_password"/>
        </div> 

        <NuxtLink to="/forgot" class="text-primary font-bold float-right mb-4">Forgot Password?</NuxtLink>
    
        <button type="submit" :class="loading.login ? 
        'btn btn-block glass bg-primary hover:bg-primary loading': 
        'btn btn-block glass bg-primary hover:bg-primary'">
          LOGIN
        </button>
        </form>
      </div>
    </div> 
    

  </div>
</template>


<script setup lang="ts">
  let loading: { login: boolean } = reactive({ login: false });

  const login_email = ref("");
  const login_password = ref("");

  const loginAccount = () => {

  };
</script>