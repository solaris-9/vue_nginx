import useAppStore from './modules/app'
import useSettingStore from './modules/settings'
import useUserStore from './modules/user'
import useTagsViewStore from './modules/tagsView';
//import usePermissionStore from './modules/permission';

const useStore = () => ({
    user: useUserStore(),
    app: useAppStore(),
    setting: useSettingStore(),
    tagsView: useTagsViewStore(),
    //permission: usePermissionStore()
  });
  
  export default useStore;