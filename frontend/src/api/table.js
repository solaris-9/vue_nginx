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

export function apiRequest(name, data) {
  switch(name) {
    case "gradeList":
      return gradeList(data);
    case "gradeAdd":
      return gradeAdd(data);
    case "gradeEdit":
      return gradeEdit(data);
    case "gradeDelete":
      return gradeDelete(data);
  };
};