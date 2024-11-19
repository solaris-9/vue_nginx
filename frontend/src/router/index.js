import {
    createRouter,
    createWebHistory
} from 'vue-router' // Import from vue-router 4
import Layout from '@/layout' // Layout import as usual
import permData from '@/utils/botton-perm-config.json' // Permission data
// Constant routes that don’t need permission checks
export const constantRoutes = [{
        path: '/login',
        component: () => import('@/views/login/index'),
        hidden: true,
    },
    {
        path: '/404',
        component: () => import('@/views/404'),
        hidden: true,
        meta: {
            accesspass: true,
            roles: []
        },
    },
    {
        path: '/',
        component: Layout,
        redirect: '/other/home',
    },
    // {
    //   path: '/home',
    //   component: () => import('@/views/home'),
    //   hidden: false,
    // },
    {
        path: '/other',
        component: Layout, // Assuming Layout is the main component for `/other`
        children: [{
            path: 'home',
            component: () => import('@/views/other/home'), // Adjust the path to the actual component
        }, ],
    },
];
// Async routes that require permission checks
export const asyncRoutes = [
    {
        path: '/admin',
        component: Layout,
        name: 'admin',
        meta: {
            title: 'Admin',
            icon: 'el-icon-user',
            roles: ["Administrator"]
        },
        children: [
            {
                path: 'grade',
                name: 'GradeManagement',
                component: () =>
                    import('@/views/admin/grade/index'),
                meta: {
                    title: 'Grade Management',
                    roles: permData['GradeManagement']['view']
                }
            },
        ]
    }, 
];

export const sigleRoutes = [];

// Create the router using createRouter and createWebHistory
const router = createRouter({
    history: createWebHistory(), // Web history mode
    routes: constantRoutes, // Set initial constant routes
    dubug: true,
});

// Reset router function for reloading routes
export function resetRouter() {
    const newRouter = createRouter({
        history: createWebHistory(),
        routes: constantRoutes, // Reset to the initial routes
    });
    router.matcher = newRouter.matcher; // Reset router matcher
}

export const awaitRoutes = constantRoutes;

export default router;