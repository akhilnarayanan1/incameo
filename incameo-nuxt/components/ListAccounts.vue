<template> 
    <label for="my_modal_6" class="btn" @click="openDialog">Load Accounts</label>
    
    <input type="checkbox" id="listAccountDialogInput" class="modal-toggle" v-model="listAccountDialogOpened" />
    <div id="listAccountDialog" class="modal"  role="dialog">
      <div class="modal-box">
        <div v-if="loading.listAccount" class="flex justify-center">
          <span class="loading loading-dots loading-lg"></span>
        </div>
        <div v-else>
          <form method="dialog">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" @click="listAccountDialogOpened = false">✕</button>
          </form>
          <h3 class="py-4 font-bold text-lg">Creator/Business Account(s)</h3>
          <ul class="menu bg-base-200  rounded-box">
            <div v-for="{picture, username, instagram_business_account} in response.connectedAccount.data">
              <li v-if="instagram_business_account">
                <a @click="saveInstgramBusinessAccount(instagram_business_account.id)"><img :src="picture.data.url" class="rounded-full w-6 h-6">{{ username }}</a>
              </li>
            </div>
          </ul>
          <h3 class="py-4 font-bold text-lg">Personal Account(s) <i>(disabled)</i></h3>
          <ul class="menu bg-base-200  rounded-box">
            <div  v-for="{picture, username, instagram_business_account} in response.connectedAccount.data">
              <li v-if="!instagram_business_account" class="disabled">
                <a><img :src="picture.data.url" class="rounded-full w-6 h-6">{{ username }}</a>
              </li>
            </div>
          </ul>
        </div>
      </div>
    </div >
</template>

<script setup lang="ts">
import { type InstagramData } from "@/assets/ts/types";
import { doc, setDoc, serverTimestamp } from "firebase/firestore";
import { useIsCurrentUserLoaded } from "vuefire";

const listAccountDialogOpened = ref(false);
const loading = reactive({page: true, listAccount: false});

const db =  useFirestore();
const currentUser = useCurrentUser();
const props = defineProps<{accessToken: string}>();
const emit = defineEmits(["loadProfile"]);

onMounted(() => { 
  watch([() => currentUser.value, () => props.accessToken], ([newCurrentUser, newAccessToken]) => {
    if(newCurrentUser && newAccessToken) {
      openDialog();
    }
  });
});

const openDialog = () => {
  listAccountDialogOpened.value = true;
  loading.listAccount = true;
  if (!useIsCurrentUserLoaded().value) {
      watch(() => currentUser, (newCurrentUser) => loadAccounts());
  } else {
    loadAccounts();
  }
};

const saveInstgramBusinessAccount = async (instagram_business_account_id: string) => {
    await setDoc(doc(db, "instagram_business", instagram_business_account_id), {
      "userid": currentUser.value?.uid,
      "lastUpdatedOn": serverTimestamp(),
    }, { merge: true })
    .then(()=>{
      loading.listAccount = false;
      addToast({message: "Account set as default", type:"success", duration: 3000});
      emit("loadProfile", {accountId: instagram_business_account_id, accessToken: props.accessToken});
      listAccountDialogOpened.value = false;
    })
    .catch(error => {
      loading.listAccount = false;
      addToast({message: error, type:"error", duration: 3000});
      listAccountDialogOpened.value = false;
    });
};

const response: { connectedAccount: InstagramData } = reactive({ connectedAccount: {} as InstagramData });

const loadAccounts = async () => {
    //Stop processing if user is blank
    if (!currentUser.value) {
      addToast({ message: "Unknown error, Please try again (401)", type: "error", duration: 3000 });
      listAccountDialogOpened.value = false;
      return;
    };
    const url = await listAccounts({accessToken: props.accessToken});
    const {pending, data: resp, error} = useLazyFetch(url, {server: false});
    watch(() => pending.value, (newpending) => {
      loading.listAccount = newpending;
      if(error.value) {
        addToast({message: error.value.data?.error?.message, type: "error", duration: 3000});
        listAccountDialogOpened.value = false;
      } else {
        response.connectedAccount = resp.value as InstagramData;
      }
    });
    loading.listAccount = pending.value;

}    

</script>