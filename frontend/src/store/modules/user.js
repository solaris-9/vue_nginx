import { loginApi, logoutApi, userInfoApi } from '@/api/user';
import {
  getToken,
  setToken,
  removeToken,
  getUserCookie,
  setUserCookie,
  removeUserCookie
} from '@/utils/auth';
import { resetRouter } from '@/router/';
import { defineStore } from 'pinia';

const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    token: getToken() || '',
    name: '',
    avatar: '',
    info: {
      name: '',
      mail: '',
      roles: '',
      level: '',
      add: '',
      edit: '',
      delete: '',
      search: '',
      view: '',
      export: '',
      download: ''
    }
  }),
  actions: {
    async RESET_STATE () {
      this.$reset();
    },

    async login (userInfo) {
      const { username, password } = userInfo;
      let result = await loginApi({
        username: username.trim(),
        password: password
      });

      if (result.code === 20000) {
        //pinia存储token

        this.token = result.data.token;

        //本地持久化存储token
        setToken(result.data.token);
        let tkk = getToken();

        return 'ok';
      } else {
        return Promise.reject(new Error('failed'));
      }
    },
    getUserInfo () {
      return new Promise((resolve, reject) => {
        userInfoApi(this.token)
          .then(response => {
            const { data } = response;
            if (!data) {
              return reject('Verification failed, please Login again.');
            }

            //const { name, avatar } = data;

            this.name = data.name;
            this.avatar = data.avatar;
            this.info.name = data.name;
            this.info.mail = data.mail;
            this.info.roles = data.roles;
            this.info.level = data.level;
            this.info.add = data.add;
            this.info.edit = data.edit;
            this.info.delete = data.delete;
            this.info.search = data.search;
            this.info.view = data.view;
            this.info.export = data.export;
            this.info.download = data.download;
            resolve(data);
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    logout () {
      return new Promise((resolve, reject) => {
        logoutApi({token: this.token, username: this.name})
          .then(() => {
            removeToken(); // must remove  token  first
            removeUserCookie();
            resetRouter();
            this.RESET_STATE();
            resolve();
          })
          .catch(error => {
            reject(error);
          });
      });
    },
    getTokenValue () {
      if (this.token) {
        return this.token;
      } else {
        const token = getToken();
        return token;
      }
    },

    resetToken () {
      return new Promise(resolve => {
        removeToken(); // must remove  token  first
        this.RESET_STATE();
        resolve();
      });
    },

    getUser () {
      if (this.info) {
        return this.info;
      } else {
        const info = getUserCookie();
        return info;
      }
    },

    checkPermission (item) {
      let info = this.getUser();
      if (info[item] == 'Yes') {
        return true;
      } else {
        return false;
      }
    }
  }
});

export default useUserStore;
