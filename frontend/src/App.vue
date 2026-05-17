<script setup>
import { onMounted } from 'vue'
import NavBar from "@/components/navbar/NavBar.vue";
import { useRouter, useRoute } from 'vue-router';
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";
const user=useUserStore()
const router=useRouter()
const route=useRoute()
onMounted(async()=>
{
    try
    {
      const res=await api.get('api/user/account/get_user_info')
      const data=res.data
      if(data.result==='success')
      {
        user.setUserInfo(data)
      }
    }
    catch (err)
    {

    }
    finally {
      user.setHasPulledUserInfo(true)
      if(route.meta.needLogin&&!user.isLogin())
      {
        await router.replace({
          name:'user-account-login-index'
        })
      }
    }
})
</script>

<template>
    <NavBar>
      <RouterView/>
    </NavBar>
</template>

<style scoped>

</style>
