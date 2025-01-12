import request from '@/utils/request'

/**
 * @description: According to the table data, the header required for producing ag-grid-vue
 * @param {arry} rowData ag-grid-vue table data
 * @returns {arry} [columnDefs, rowData]
 */
export function getGridData(rowData) {
  let table_head = rowData[0]
  let columnDefs = []
  for (let k in table_head) {
      let item = { field: k, headerName: k, headerTooltip: k, filterParams: { applyMiniFilterWhileTyping: true }, autoHeight: true, wrapText: true }
      if (k.toUpperCase() === "ID") { item.hide = true }
      columnDefs.push(item)
  }
  return [columnDefs, rowData]
};

export function getList(data) {
  return request({
    url: '/api/table/list',
    method: 'get',
    data
  })
};

export function gradeList(params) {
  console.log("params = ", params)
  return request({
      url: '/grade/grade_list',
      method: 'get',
      params
  })
};
export function gradeEdit(data) {
  return request({
      url: '/grade/grade_edit',
      method: 'put',
      data
  })
};
export function gradeAdd(data) {
  return request({
      url: '/grade/grade_edit',
      method: 'post',
      data
  })
};
export function gradeDelete(data) {
  return request({
      url: '/grade/grade_delete',
      method: 'post',
      data
  })
};

export function userList(params) {
  console.log("params = ", params)
  return request({
      url: '/user/list',
      method: 'get',
      params
  })
};
export function userEdit(data) {
  return request({
      url: '/user/edit',
      method: 'put',
      data
  })
};
export function userAdd(data) {
  return request({
      url: '/user/edit',
      method: 'post',
      data
  })
};
export function userDelete(data) {
  return request({
      url: '/user/delete',
      method: 'post',
      data
  })
};

export function deviceDpList(params) {
  console.log("params = ", params)
  return request({
      url: '/devicedp/list',
      method: 'get',
      params
  })
};
export function deviceDpEdit(data) {
  return request({
      url: '/devicedp/edit',
      method: 'put',
      data
  })
};
export function deviceDpAdd(data) {
  return request({
      url: '/devicedp/edit',
      method: 'post',
      data
  })
};
export function deviceDpDelete(data) {
  return request({
      url: '/devicedp/delete',
      method: 'post',
      data
  })
};

export function platformList(params) {
  console.log("params = ", params)
  return request({
      url: '/platform/list',
      method: 'get',
      params
  })
};
export function platformEdit(data) {
  return request({
      url: '/platform/edit',
      method: 'put',
      data
  })
};
export function platformAdd(data) {
  return request({
      url: '/platform/edit',
      method: 'post',
      data
  })
};
export function platformDelete(data) {
  return request({
      url: '/platform/delete',
      method: 'post',
      data
  })
};

export function NwccList(params) {
  console.log("params = ", params)
  return request({
      url: '/nwcc/list',
      method: 'get',
      params
  })
};
export function nwccEdit(data) {
  return request({
      url: '/nwcc/edit',
      method: 'put',
      data
  })
};
export function nwccAdd(data) {
  return request({
      url: '/nwcc/edit',
      method: 'post',
      data
  })
};
export function nwccDelete(data) {
  return request({
      url: '/nwcc/delete',
      method: 'post',
      data
  })
};

export function roleList(params) {
  return request({
      url: '/grade/role_list',
      method: 'get',
      params
  })
};
export function customerList(params) {
  return request({
      url: '/common/customer_list',
      method: 'get',
      params
  })
};
export function deviceList(params) {
  return request({
      url: '/common/device_list',
      method: 'get',
      params
  })
};
export function nwccList(params) {
  return request({
      url: '/common/nwcc_list',
      method: 'get',
      params
  })
};
export function countryList(params) {
  return request({
      url: '/common/country_list',
      method: 'get',
      params
  })
};
export function hostingList(params) {
  return request({
      url: '/common/hosting_list',
      method: 'get',
      params
  })
};

export function contactsList(params) {
  return request({
      url: '/customer/list',
      method: 'get',
      params
  })
};
export function customerEdit(data) {
  return request({
      url: '/customer/edit',
      method: 'put',
      data
  })
};
export function customerAdd(data) {
  return request({
      url: '/customer/edit',
      method: 'post',
      data
  })
};

// export function apiRequestBak(name, data) {
//   switch(name) {
//     case "gradeList":
//       return gradeList(data);
//     case "gradeAdd":
//       return gradeAdd(data);
//     case "gradeEdit":
//       return gradeEdit(data);
//     case "gradeDelete":
//       return gradeDelete(data);

//     case "userList":
//       return userList(data);
//     case "userAdd":
//       return userAdd(data);
//     case "userEdit":
//       return userEdit(data);
//     case "userDelete":
//       return userDelete(data);

//     case "deviceDpList":
//       return deviceDpList(data);
//     case "deviceDpAdd":
//       return deviceDpAdd(data);
//     case "deviceDpEdit":
//       return deviceDprEdit(data);
//     case "deviceDpDelete":
//       return deviceDpDelete(data);

//     case "roleList":
//       return roleList(data);
//     case "customerList":
//       return customerList(data);
//   };
// };

const apiFunctions = {
  gradeList,
  gradeAdd,
  gradeEdit,
  gradeDelete,

  userList,
  userAdd,
  userEdit,
  userDelete,

  deviceDpList,
  deviceDpAdd,
  deviceDpEdit,
  deviceDpDelete,

  platformList,
  platformAdd,
  platformEdit,
  platformDelete,

  NwccList,
  nwccAdd,
  nwccEdit,
  nwccDelete,

  roleList,
  customerList,
  deviceList,
  nwccList,
  contactsList,
  countryList,
  hostingList,
  
  customerAdd,
  customerEdit
};

export function apiRequest(name, data) {
  //console.log("apiFunctions = ", apiFunctions)
  //console.log("apiFunction = ", apiFunctions[name])
  const apiFunction = apiFunctions[name];
  if (!apiFunction) {
      throw new Error(`API function not found for name: ${name}`);
  }
  return apiFunction(data);
}
