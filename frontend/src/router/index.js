import { createRouter, createWebHashHistory } from "vue-router";
import Layout from "@/layout/index.vue";

export const constantRoutes = [
  {
    path: "/login",
    component: () => import("@/views/login/index.vue"),
    hidden: true,
  },

  {
    path: "/404",
    component: () => import("@/views/404.vue"),
    hidden: true,
  },
  {
    path: '/redirect',
    component: Layout,
    meta: { hidden: true },
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index.vue')
      }
    ]
  },

  {
    path: "/",
    component: Layout,
    hidden: true,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("@/views/dashboard/index.vue"),
        meta: { title: "Home", icon: "home" },
      },
    ],
  },

  {
    path: "/tools",
    component: Layout,
    redirect: "/tools/devicedp",
    name: "Home",
    meta: { title: "Home", icon: "Grid" },
    children: [
      {
        path: "nwcc",
        name: "NWCC",
        component: () => import("@/views/nwcc/index.vue"),
        meta: { title: "Home Controller Deployment", icon: "check" },
      },     
      {
        path: "devicedp",
        name: "Devicedp",
        component: () => import("@/views/devicedp/index.vue"),
        meta: { title: "Device Deployment", icon: "Check" },
      },     
      {
        path: "contacts",
        name: "Contacts",
        component: () => import("@/views/customer/index.vue"),
        meta: { title: "Customer Contacts", icon: "Check" },
      },     
      {
        path: "platform",
        name: "Platform",
        component: () => import("@/views/platform/index.vue"),
        meta: { title: "Corteca Platform", icon: "Check", checkPermission: true },
        // hidden: checkPermission()
      },     
    ],
  },

  {
    path: "/admin",
    component: Layout,
    redirect: "/admin/grade",
    name: "Admin",
    meta: { title: "Admin", icon: "UserFilled", checkPermission: true },
    children: [
      {
        path: "grade",
        name: "Grade",
        component: () => import("@/views/grade/index.vue"),
        meta: { title: "Grade Management", icon: "Check" },
      },     
      {
        path: "user",
        name: "User",
        component: () => import("@/views/user/index.vue"),
        meta: { title: "User Management", icon: "Check" },
      },
    ],
  },

  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("@/views/404.vue"),
    hidden: true,
  },
];
const createRoute = () =>
  createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: constantRoutes,
    scrollBehavior: () => ({ left: 0, top: 0 }),
  });

const router = createRoute();

export function resetRouter() {
  const newRouter = createRoute();
  router.matcher = newRouter.matcher; // reset router
}

export default router;
