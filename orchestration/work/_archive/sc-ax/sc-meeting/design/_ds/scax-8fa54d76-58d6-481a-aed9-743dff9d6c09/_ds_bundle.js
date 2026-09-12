/* @ds-bundle: {"namespace":"SCAX","components":[{"name":"Checkbox","sourcePath":"components/general/Checkbox/Checkbox.jsx"},{"name":"ConfirmModal","sourcePath":"components/general/ConfirmModal/ConfirmModal.jsx"},{"name":"DateField","sourcePath":"components/general/DateField/DateField.jsx"},{"name":"DatePicker","sourcePath":"components/general/DatePicker/DatePicker.jsx"},{"name":"Drawer","sourcePath":"components/general/Drawer/Drawer.jsx"},{"name":"Empty","sourcePath":"components/general/Empty/Empty.jsx"},{"name":"EmptyValue","sourcePath":"components/general/EmptyValue/EmptyValue.jsx"},{"name":"FieldMessage","sourcePath":"components/general/FieldMessage/FieldMessage.jsx"},{"name":"Icon","sourcePath":"components/general/Icon/Icon.jsx"},{"name":"MinWidthNotice","sourcePath":"components/general/MinWidthNotice/MinWidthNotice.jsx"},{"name":"Popover","sourcePath":"components/general/Popover/Popover.jsx"},{"name":"ProgressBar","sourcePath":"components/general/ProgressBar/ProgressBar.jsx"},{"name":"Skeleton","sourcePath":"components/general/Skeleton/Skeleton.jsx"},{"name":"TaskCalendar","sourcePath":"components/general/TaskCalendar/TaskCalendar.jsx"},{"name":"Toast","sourcePath":"components/general/Toast/Toast.jsx"}],"sourceHashes":{"components/general/Checkbox/Checkbox.jsx":"dd8e7efb3498","components/general/Checkbox/Checkbox.d.ts":"9a74cf880d10","components/general/Checkbox/Checkbox.prompt.md":"c3041e5f1f30","components/general/ConfirmModal/ConfirmModal.jsx":"39a275b3003f","components/general/ConfirmModal/ConfirmModal.d.ts":"2673e23f15e8","components/general/ConfirmModal/ConfirmModal.prompt.md":"9daf7f7c6ded","components/general/DateField/DateField.jsx":"33b7df7a5bd6","components/general/DateField/DateField.d.ts":"e957266ee2c3","components/general/DateField/DateField.prompt.md":"6443103a8559","components/general/DatePicker/DatePicker.jsx":"51ebe7d8558d","components/general/DatePicker/DatePicker.d.ts":"df27597a25d5","components/general/DatePicker/DatePicker.prompt.md":"434b9557fa7a","components/general/Drawer/Drawer.jsx":"0fd28f811cab","components/general/Drawer/Drawer.d.ts":"1ca652667475","components/general/Drawer/Drawer.prompt.md":"9e9904e351eb","components/general/Empty/Empty.jsx":"38f131a032e2","components/general/Empty/Empty.d.ts":"4338ef938c81","components/general/Empty/Empty.prompt.md":"ddc2520314d8","components/general/EmptyValue/EmptyValue.jsx":"305b0f8c1483","components/general/EmptyValue/EmptyValue.d.ts":"fdffccf7391b","components/general/EmptyValue/EmptyValue.prompt.md":"7e0f4eca2f1d","components/general/FieldMessage/FieldMessage.jsx":"8ff83d48fb22","components/general/FieldMessage/FieldMessage.d.ts":"ef20d923e487","components/general/FieldMessage/FieldMessage.prompt.md":"2cef24a61c65","components/general/Icon/Icon.jsx":"dee942274f6e","components/general/Icon/Icon.d.ts":"8fe63030594f","components/general/Icon/Icon.prompt.md":"165a2b4e1ecc","components/general/MinWidthNotice/MinWidthNotice.jsx":"cb703854de36","components/general/MinWidthNotice/MinWidthNotice.d.ts":"71c5d8da96a5","components/general/MinWidthNotice/MinWidthNotice.prompt.md":"3e525aa45ca7","components/general/Popover/Popover.jsx":"803444849bda","components/general/Popover/Popover.d.ts":"adf9aeb3d203","components/general/Popover/Popover.prompt.md":"8f86b6dcbbe2","components/general/ProgressBar/ProgressBar.jsx":"f9bc8b4eb15e","components/general/ProgressBar/ProgressBar.d.ts":"d998296ad69b","components/general/ProgressBar/ProgressBar.prompt.md":"fa12057920bf","components/general/Skeleton/Skeleton.jsx":"03e0ab066ab1","components/general/Skeleton/Skeleton.d.ts":"f19aa34f2e64","components/general/Skeleton/Skeleton.prompt.md":"8f28d00877f5","components/general/TaskCalendar/TaskCalendar.jsx":"290da2d79c41","components/general/TaskCalendar/TaskCalendar.d.ts":"84b247bec0fc","components/general/TaskCalendar/TaskCalendar.prompt.md":"230e203545e9","components/general/Toast/Toast.jsx":"943fa8858dfe","components/general/Toast/Toast.d.ts":"6b629be13cc9","components/general/Toast/Toast.prompt.md":"1d989c4fc098"},"inlinedExternals":[],"builtBy":"cc-design-sync"} */
"use strict";
var SCAX = (() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __esm = (fn, res, err) => function __init() {
    if (err) throw err[0];
    try {
      return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
    } catch (e) {
      throw err = [e], e;
    }
  };
  var __commonJS = (cb, mod) => function __require() {
    try {
      return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
    } catch (e) {
      throw mod = 0, e;
    }
  };
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
    // If the importer is in node compatibility mode or this is not an ESM
    // file that has been converted to a CommonJS file using a Babel-
    // compatible transform (i.e. "__esModule" has not been set), then set
    // "default" to the CommonJS "module.exports" for node compatibility.
    isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
    mod
  ));
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // <define:import.meta.env>
  var init_define_import_meta_env = __esm({
    "<define:import.meta.env>"() {
    }
  });

  // shim:react-shim
  var require_react_shim = __commonJS({
    "shim:react-shim"(exports, module) {
      init_define_import_meta_env();
      var R = window.React;
      function np(p, k) {
        var o = {};
        for (var x in p) if (x !== "children") o[x] = p[x];
        if (k !== void 0) o.key = k;
        return o;
      }
      function jsx13(t, p, k) {
        var c = p && p.children;
        return c === void 0 ? R.createElement(t, np(p, k)) : R.createElement(t, np(p, k), c);
      }
      function jsxs13(t, p, k) {
        return R.createElement.apply(R, [t, np(p, k)].concat(p.children));
      }
      module.exports = R;
      module.exports.jsx = jsx13;
      module.exports.jsxs = jsxs13;
      module.exports.jsxDEV = function(t, p, k, s) {
        return (s ? jsxs13 : jsx13)(t, p, k);
      };
      module.exports.Fragment = R.Fragment;
    }
  });

  // frontend/ds-entry.tsx
  var ds_entry_exports = {};
  __export(ds_entry_exports, {
    Checkbox: () => Checkbox,
    ConfirmModal: () => ConfirmModal,
    DateField: () => DateField,
    DatePicker: () => DatePicker,
    Drawer: () => Drawer,
    Empty: () => Empty,
    EmptyValue: () => EmptyValue,
    FieldMessage: () => FieldMessage,
    Icon: () => Icon,
    MinWidthNotice: () => MinWidthNotice,
    Popover: () => Popover,
    ProgressBar: () => ProgressBar,
    Skeleton: () => Skeleton,
    TaskCalendar: () => TaskCalendar,
    Toast: () => Toast
  });
  init_define_import_meta_env();

  // frontend/src/Icon.tsx
  init_define_import_meta_env();
  var import_jsx_runtime = __toESM(require_react_shim(), 1);
  var paths = {
    close: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M4 4l8 8M12 4l-8 8" }),
    "chevron-down": /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "m4 6 4 4 4-4" }),
    "chevron-right": /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "m6 4 4 4-4 4" }),
    "arrow-right": /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M3 8h10M9 4l4 4-4 4" }),
    "arrow-up": /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M8 13V3.5M4 7.5l4-4 4 4" }),
    "arrow-down": /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M8 3v9.5M4 8.5l4 4 4-4" }),
    // v2 08 의 AI 버튼이 쓰는 별 — 문서의 path 그대로
    sparkle: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M8 2.5 9.3 6l3.2 1.3L9.3 8.6 8 12l-1.3-3.4L3.5 7.3 6.7 6 8 2.5Z" }),
    send: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M13.5 8 3 3.5 4.6 8 3 12.5 13.5 8ZM4.6 8h8.9" }),
    // v2 09 의 체크박스가 쓰는 체크 — 문서의 path 그대로
    check: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "m3.5 8.5 3 3 6-6" }),
    "check-square": /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", { height: "11", rx: "2", width: "11", x: "2.5", y: "2.5" }),
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "m5.5 8 2 2 3.5-3.5" })
    ] }),
    square: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", { height: "11", rx: "2", width: "11", x: "2.5", y: "2.5" }),
    circle: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("circle", { cx: "8", cy: "8", r: "5" }),
    play: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M6.5 4.3 11.5 8l-5 3.7Z" }),
    // v2 07 의 20px 목록 글리프 — 문서의 path 그대로
    list: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M3 4.5h10M3 8h10M3 11.5h6" }),
    // v2 09 의 날짜 필드 글리프 — 문서의 path 그대로
    calendar: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", { height: "10", rx: "2", width: "11", x: "2.5", y: "3.5" }),
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M2.5 6.5h11M5.5 2v3M10.5 2v3" })
    ] }),
    paperclip: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M11.8 7.3 7.2 11.9a2.4 2.4 0 0 1-3.4-3.4l5.3-5.3a1.7 1.7 0 0 1 2.4 2.4l-5.3 5.3a1 1 0 0 1-1.4-1.4l4.6-4.6" }),
    plus: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M8 3.5v9M3.5 8h9" }),
    minus: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M3.5 8h9" }),
    home: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "m2.5 7.6 5.5-4.6 5.5 4.6M4.2 7v6.5h7.6V7" }),
    refresh: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M13 8a5 5 0 1 1-1.7-3.8M13.2 2.4V5.2h-2.8" }),
    ban: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("circle", { cx: "8", cy: "8", r: "5.5" }),
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "m4.1 11.9 7.8-7.8" })
    ] }),
    pending: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("circle", { cx: "8", cy: "8", r: "5.5", strokeDasharray: "2.2 2.2" }),
    alert: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("circle", { cx: "8", cy: "8", r: "5.5" }),
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M8 5v3.6M8 10.8h.01" })
    ] }),
    // v2 07 의 16px 기본 글리프 — 문서의 path 그대로
    search: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("circle", { cx: "7.2", cy: "7.2", r: "4.4" }),
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "m10.6 10.6 2.6 2.6" })
    ] }),
    // v2 10 의 빈 상태 글리프 — 문서의 path 그대로
    empty: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("rect", { height: "10", rx: "2", width: "11", x: "2.5", y: "3.5" }),
      /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M5.5 7.5h5M5.5 10h3" })
    ] }),
    filter: /* @__PURE__ */ (0, import_jsx_runtime.jsx)("path", { d: "M2.8 3.5h10.4l-4 4.8v4.2l-2.4-1.6V8.3l-4-4.8Z" })
  };
  function Icon({
    name,
    size = 16,
    className,
    title
  }) {
    return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(
      "svg",
      {
        "aria-hidden": title ? void 0 : true,
        className,
        fill: "none",
        focusable: "false",
        height: size,
        role: title ? "img" : void 0,
        stroke: "currentColor",
        strokeLinecap: "round",
        strokeLinejoin: "round",
        strokeWidth: size <= 14 ? 1.3 : 1.5,
        viewBox: "0 0 16 16",
        width: size,
        children: [
          title && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("title", { children: title }),
          paths[name]
        ]
      }
    );
  }

  // frontend/src/Popover.tsx
  init_define_import_meta_env();
  var import_react = __toESM(require_react_shim(), 1);
  var import_jsx_runtime2 = __toESM(require_react_shim(), 1);
  function Popover({
    trigger,
    children,
    label,
    width = 200
  }) {
    const [open, setOpen] = (0, import_react.useState)(false);
    const [above, setAbove] = (0, import_react.useState)(false);
    const rootRef = (0, import_react.useRef)(null);
    const panelRef = (0, import_react.useRef)(null);
    const panelId = (0, import_react.useId)();
    (0, import_react.useEffect)(() => {
      if (!open) return;
      const onPointerDown = (event) => {
        if (!rootRef.current?.contains(event.target)) setOpen(false);
      };
      const onKeyDown = (event) => {
        if (event.key === "Escape") {
          setOpen(false);
          rootRef.current?.querySelector("button")?.focus();
        }
      };
      document.addEventListener("mousedown", onPointerDown);
      document.addEventListener("keydown", onKeyDown);
      return () => {
        document.removeEventListener("mousedown", onPointerDown);
        document.removeEventListener("keydown", onKeyDown);
      };
    }, [open]);
    (0, import_react.useEffect)(() => {
      if (!open || !rootRef.current || !panelRef.current) return;
      const anchor = rootRef.current.getBoundingClientRect();
      const needed = panelRef.current.offsetHeight + 8;
      setAbove(anchor.bottom + needed > window.innerHeight && anchor.top > needed);
    }, [open]);
    const toggle = () => setOpen((value) => !value);
    return /* @__PURE__ */ (0, import_jsx_runtime2.jsxs)("span", { className: "popover-root", ref: rootRef, children: [
      trigger({
        open,
        toggle,
        props: { "aria-expanded": open, "aria-haspopup": "true", "aria-controls": open ? panelId : void 0, onClick: toggle, type: "button" }
      }),
      open && /* @__PURE__ */ (0, import_jsx_runtime2.jsx)("div", { "aria-label": label, className: above ? "popover above" : "popover", id: panelId, ref: panelRef, role: "group", style: { width }, children: children(() => setOpen(false)) })
    ] });
  }

  // frontend/src/Empty.tsx
  init_define_import_meta_env();

  // frontend/src/labels.ts
  init_define_import_meta_env();
  var taskStateLabel = {
    open: "시작 전",
    in_progress: "진행 중",
    blocked: "막힘",
    completion_submitted: "완료 확인 대기",
    done: "완료",
    cancelled: "취소"
  };
  function seoulToday() {
    return (/* @__PURE__ */ new Date()).toLocaleDateString("en-CA", { timeZone: "Asia/Seoul" });
  }
  function formatDate(isoDate) {
    if (!isoDate) return "—";
    const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(isoDate);
    return match ? `${match[1]}/${match[2]}/${match[3]}` : isoDate;
  }
  function formatMonth(year, month) {
    return `${String(year).padStart(4, "0")}/${String(month).padStart(2, "0")}`;
  }
  function formatMonthLong(year, month) {
    return `${year}년 ${month}월`;
  }
  function addDays(isoDate, days) {
    const [year, month, day] = isoDate.split("-").map(Number);
    const date = new Date(Date.UTC(year, month - 1, day + days));
    return date.toISOString().slice(0, 10);
  }
  var emptyActionLabel = {
    filter: "필터 초기화",
    error: "다시 시도"
  };
  var taskFilterLabel = {
    active: "진행 중\xB7시작 전\xB7막힘",
    all: "전체 상태",
    ...taskStateLabel
  };
  var emptyValue = "—";
  var minWidthNotice = {
    title: "화면이 좁습니다",
    description: "가로 1280 이상에서 사용해 주세요. 창을 넓히면 바로 이어서 볼 수 있습니다."
  };
  var weekdayNames = ["일", "월", "화", "수", "목", "금", "토"];
  var datePickerLabel = {
    open: "달력 열기",
    previousMonth: "이전 달",
    nextMonth: "다음 달",
    clear: "지우기",
    today: "오늘"
  };

  // frontend/src/Empty.tsx
  var import_jsx_runtime3 = __toESM(require_react_shim(), 1);
  function Empty({
    title,
    description,
    variant = "default",
    actionLabel,
    onAction,
    className,
    children
  }) {
    const label = actionLabel ?? (variant === "default" ? void 0 : emptyActionLabel[variant]);
    const icon = variant === "error" ? "alert" : variant === "filter" ? "filter" : "empty";
    return /* @__PURE__ */ (0, import_jsx_runtime3.jsxs)(
      "div",
      {
        className: ["empty-state", variant === "default" ? "" : variant, className ?? ""].filter(Boolean).join(" "),
        role: variant === "error" ? "alert" : void 0,
        children: [
          /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("span", { "aria-hidden": true, className: "empty-icon", children: /* @__PURE__ */ (0, import_jsx_runtime3.jsx)(Icon, { name: icon, size: 20 }) }),
          /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("b", { children: title }),
          description && /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("p", { children: description }),
          onAction && label && /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("button", { className: "btn", onClick: onAction, type: "button", children: label }),
          children
        ]
      }
    );
  }
  function EmptyValue() {
    return /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("span", { className: "empty-value", children: emptyValue });
  }

  // frontend/src/Skeleton.tsx
  init_define_import_meta_env();
  var import_jsx_runtime4 = __toESM(require_react_shim(), 1);
  function Skeleton({ rows = 5, label = "불러오는 중" }) {
    return /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)("div", { "aria-busy": "true", className: "skeleton", role: "status", children: [
      /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("span", { className: "sr-only", children: label }),
      Array.from({ length: rows }, (_, index) => /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("span", { "aria-hidden": true, className: "skeleton-bar" }, index))
    ] });
  }

  // frontend/src/ProgressBar.tsx
  init_define_import_meta_env();
  var import_jsx_runtime5 = __toESM(require_react_shim(), 1);
  function ProgressBar({ label, done, total }) {
    const percent = total > 0 ? Math.round(done / total * 100) : 0;
    return /* @__PURE__ */ (0, import_jsx_runtime5.jsxs)("div", { className: "progress", children: [
      label && /* @__PURE__ */ (0, import_jsx_runtime5.jsxs)("div", { className: "progress-head", children: [
        /* @__PURE__ */ (0, import_jsx_runtime5.jsx)("b", { children: label }),
        /* @__PURE__ */ (0, import_jsx_runtime5.jsxs)("span", { className: "t-meta", children: [
          done,
          " / ",
          total
        ] })
      ] }),
      /* @__PURE__ */ (0, import_jsx_runtime5.jsx)(
        "div",
        {
          "aria-label": label ?? "진행률",
          "aria-valuemax": total,
          "aria-valuemin": 0,
          "aria-valuenow": done,
          className: "progress-track",
          role: "progressbar",
          children: /* @__PURE__ */ (0, import_jsx_runtime5.jsx)("span", { className: "progress-fill", style: { width: `${percent}%` } })
        }
      )
    ] });
  }

  // frontend/src/Modal.tsx
  init_define_import_meta_env();
  var import_react2 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime6 = __toESM(require_react_shim(), 1);
  function useEscape(onClose) {
    (0, import_react2.useEffect)(() => {
      const onKeyDown = (event) => {
        if (event.key === "Escape") onClose();
      };
      window.addEventListener("keydown", onKeyDown);
      return () => window.removeEventListener("keydown", onKeyDown);
    }, [onClose]);
  }
  function Drawer({
    label,
    kicker,
    title,
    headerExtra,
    footer,
    onClose,
    children
  }) {
    useEscape(onClose);
    return /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)(import_jsx_runtime6.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("div", { "aria-hidden": true, className: "overlay-scrim", onMouseDown: onClose }),
      /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)("section", { "aria-label": label, "aria-modal": "true", className: "drawer", role: "dialog", children: [
        /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)("header", { className: "drawer-head", children: [
          /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)("div", { style: { minWidth: 0 }, children: [
            kicker && /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("small", { className: "modal-kicker", children: kicker }),
            /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("h3", { children: title }),
            headerExtra
          ] }),
          /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("button", { "aria-label": "상세 닫기", className: "modal-close", onClick: onClose, type: "button", children: /* @__PURE__ */ (0, import_jsx_runtime6.jsx)(Icon, { name: "close" }) })
        ] }),
        /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("div", { className: "drawer-body", children }),
        footer && /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("footer", { className: "drawer-foot", children: footer })
      ] })
    ] });
  }
  function ConfirmModal({
    title,
    description,
    confirmLabel,
    danger = false,
    busy = false,
    onConfirm,
    onClose
  }) {
    useEscape(onClose);
    return /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("div", { className: "modal-backdrop", onMouseDown: (event) => event.target === event.currentTarget && onClose(), children: /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)("section", { "aria-label": title, "aria-modal": "true", className: "modal", role: "alertdialog", children: [
      /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("header", { className: "modal-head", children: /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("h3", { children: title }) }),
      /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("div", { className: "modal-body", children: /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("p", { children: description }) }),
      /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)("footer", { className: "modal-foot", children: [
        /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("button", { className: "btn h40 ghost", disabled: busy, onClick: onClose, type: "button", children: "돌아가기" }),
        /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("button", { className: danger ? "btn h40 danger" : "btn h40 primary", disabled: busy, onClick: onConfirm, type: "button", children: confirmLabel })
      ] })
    ] }) });
  }
  function Toast({
    message,
    onClose,
    action,
    tone
  }) {
    (0, import_react2.useEffect)(() => {
      const timer = window.setTimeout(onClose, 4e3);
      return () => window.clearTimeout(timer);
    }, [message, onClose]);
    return (
      // 실패는 읽던 자리를 끊고 알려야 한다 — 그때만 role 을 alert 로 올린다.
      /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)("div", { className: tone ? `toast ${tone}` : "toast", role: tone === "error" ? "alert" : "status", children: [
        tone ? /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)("span", { className: "toast-message", children: [
          /* @__PURE__ */ (0, import_jsx_runtime6.jsx)(Icon, { className: "toast-icon", name: tone === "success" ? "check" : "alert" }),
          message
        ] }) : message,
        action && /* @__PURE__ */ (0, import_jsx_runtime6.jsx)(
          "button",
          {
            className: "toast-action",
            onClick: () => {
              action.onAction();
              onClose();
            },
            type: "button",
            children: action.label
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("button", { "aria-label": "알림 지우기", onClick: onClose, type: "button", children: /* @__PURE__ */ (0, import_jsx_runtime6.jsx)(Icon, { name: "close" }) })
      ] })
    );
  }

  // frontend/src/FormControls.tsx
  init_define_import_meta_env();
  var import_jsx_runtime7 = __toESM(require_react_shim(), 1);
  function Checkbox({
    checked,
    onChange,
    disabled,
    id,
    children
  }) {
    return /* @__PURE__ */ (0, import_jsx_runtime7.jsxs)("label", { className: "checkbox", children: [
      /* @__PURE__ */ (0, import_jsx_runtime7.jsxs)("span", { className: "checkbox-box", children: [
        /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("input", { checked, disabled, id, onChange: (event) => onChange(event.target.checked), type: "checkbox" }),
        /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("svg", { "aria-hidden": true, fill: "none", stroke: "currentColor", strokeLinecap: "round", strokeLinejoin: "round", strokeWidth: "2.2", viewBox: "0 0 16 16", children: /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("path", { d: "m3.5 8.5 3 3 6-6" }) })
      ] }),
      children != null && /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("span", { className: "checkbox-label", children })
    ] });
  }
  function FieldMessage({ error, help, id }) {
    if (error) {
      return /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("p", { className: "field-error", id, role: "alert", children: error });
    }
    if (help) {
      return /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("p", { className: "field-help", id, children: help });
    }
    return null;
  }

  // frontend/src/DateField.tsx
  init_define_import_meta_env();
  var import_react3 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime8 = __toESM(require_react_shim(), 1);
  var ISO = /^(\d{4})-(\d{2})-(\d{2})$/;
  function parseDateInput(text) {
    const digits = text.replace(/[^\d]/g, "");
    if (digits.length !== 8) return null;
    const iso = `${digits.slice(0, 4)}-${digits.slice(4, 6)}-${digits.slice(6, 8)}`;
    const match = ISO.exec(iso);
    if (!match) return null;
    const [, year, month, day] = match;
    const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)));
    const round = date.toISOString().slice(0, 10);
    return round === iso ? iso : null;
  }
  function DateField({
    id,
    label,
    value,
    onChange,
    disabled = false,
    hideLabel = false
  }) {
    const [text, setText] = (0, import_react3.useState)(() => value ? formatDate(value) : "");
    const pickerId = (0, import_react3.useId)();
    const picker = (0, import_react3.useRef)(null);
    (0, import_react3.useEffect)(() => {
      setText(value ? formatDate(value) : "");
    }, [value]);
    const commit = (next) => {
      setText(next);
      const trimmed = next.trim();
      if (!trimmed) {
        onChange("");
        return;
      }
      const parsed = parseDateInput(trimmed);
      if (parsed) onChange(parsed);
    };
    return /* @__PURE__ */ (0, import_jsx_runtime8.jsxs)("div", { className: "date-field", children: [
      /* @__PURE__ */ (0, import_jsx_runtime8.jsx)("label", { className: hideLabel ? "sr-only" : void 0, htmlFor: id, children: label }),
      /* @__PURE__ */ (0, import_jsx_runtime8.jsxs)("div", { className: "date-field-control", children: [
        /* @__PURE__ */ (0, import_jsx_runtime8.jsx)(
          "input",
          {
            "aria-describedby": `${pickerId}-hint`,
            autoComplete: "off",
            disabled,
            id,
            inputMode: "numeric",
            onBlur: () => setText(value ? formatDate(value) : ""),
            onChange: (event) => commit(event.target.value),
            placeholder: "YYYY/MM/DD",
            type: "text",
            value: text
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime8.jsx)(
          "button",
          {
            "aria-label": `${label} 달력 열기`,
            className: "btn h30 ghost date-field-picker",
            disabled,
            onClick: () => {
              const element = picker.current;
              if (!element) return;
              if (typeof element.showPicker === "function") element.showPicker();
              else element.focus();
            },
            type: "button",
            children: /* @__PURE__ */ (0, import_jsx_runtime8.jsx)(Icon, { name: "calendar", size: 14 })
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime8.jsx)(
          "input",
          {
            "aria-hidden": true,
            className: "sr-only",
            disabled,
            onChange: (event) => onChange(event.target.value),
            ref: picker,
            tabIndex: -1,
            type: "date",
            value
          }
        )
      ] }),
      /* @__PURE__ */ (0, import_jsx_runtime8.jsx)("span", { className: "sr-only", id: `${pickerId}-hint`, children: "연도 4자리, 월 2자리, 일 2자리 순서로 입력합니다. 예: 2026/09/30" })
    ] });
  }

  // frontend/src/DatePicker.tsx
  init_define_import_meta_env();
  var import_react4 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime9 = __toESM(require_react_shim(), 1);
  function shiftMonth(isoDate, delta) {
    const [year, month, day] = isoDate.split("-").map(Number);
    const target = new Date(Date.UTC(year, month - 1 + delta, 1));
    const lastDay = new Date(Date.UTC(target.getUTCFullYear(), target.getUTCMonth() + 1, 0)).getUTCDate();
    return new Date(Date.UTC(target.getUTCFullYear(), target.getUTCMonth(), Math.min(day, lastDay))).toISOString().slice(0, 10);
  }
  function clamp(isoDate, min, max) {
    if (min && isoDate < min) return min;
    if (max && isoDate > max) return max;
    return isoDate;
  }
  function DatePickerPanel({
    value,
    onChange,
    min,
    max,
    close
  }) {
    const today = seoulToday();
    const [focus, setFocus] = (0, import_react4.useState)(() => clamp(value || today, min, max));
    const gridRef = (0, import_react4.useRef)(null);
    const moveFocus = (0, import_react4.useRef)(true);
    (0, import_react4.useEffect)(() => {
      if (!moveFocus.current) return;
      gridRef.current?.querySelector(`[data-date="${focus}"]`)?.focus();
    }, [focus]);
    const goto = (isoDate, withFocus) => {
      moveFocus.current = withFocus;
      setFocus(clamp(isoDate, min, max));
    };
    const cursor = focus.slice(0, 7);
    const [year, month] = cursor.split("-").map(Number);
    const gridStart = addDays(`${cursor}-01`, -new Date(Date.UTC(year, month - 1, 1)).getUTCDay());
    const days = Array.from({ length: 42 }, (_, index) => addDays(gridStart, index));
    const weeks = Array.from({ length: 6 }, (_, index) => days.slice(index * 7, index * 7 + 7));
    const outOfRange = (isoDate) => Boolean(min && isoDate < min || max && isoDate > max);
    const pick = (isoDate) => {
      onChange(isoDate);
      close();
    };
    const onKeyDown = (event) => {
      const step = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[event.key];
      if (step) {
        event.preventDefault();
        goto(addDays(focus, step), true);
        return;
      }
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        if (!outOfRange(focus)) pick(focus);
      }
    };
    return /* @__PURE__ */ (0, import_jsx_runtime9.jsxs)(import_jsx_runtime9.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime9.jsxs)("div", { className: "date-picker-head", children: [
        /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(
          "button",
          {
            "aria-label": datePickerLabel.previousMonth,
            className: "btn h30 icon ghost date-picker-prev",
            onClick: () => goto(shiftMonth(focus, -1), false),
            type: "button",
            children: /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(Icon, { name: "chevron-right", size: 12 })
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("span", { className: "t-item", children: formatMonthLong(year, month) }),
        /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(
          "button",
          {
            "aria-label": datePickerLabel.nextMonth,
            className: "btn h30 icon ghost",
            onClick: () => goto(shiftMonth(focus, 1), false),
            type: "button",
            children: /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(Icon, { name: "chevron-right", size: 12 })
          }
        )
      ] }),
      /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("div", { "aria-hidden": true, className: "calendar-weekdays", children: weekdayNames.map((weekday) => /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("span", { children: weekday }, weekday)) }),
      /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("div", { className: "date-picker-grid", onKeyDown, ref: gridRef, role: "grid", children: weeks.map((week) => /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("div", { className: "date-picker-row", role: "row", children: week.map((day) => /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(
        "button",
        {
          "aria-current": day === today ? "date" : void 0,
          "aria-label": formatDate(day),
          "aria-selected": day === value,
          className: ["date-picker-cell", day.startsWith(cursor) ? "" : "outside", day === today ? "today" : ""].filter(Boolean).join(" "),
          "data-date": day,
          disabled: outOfRange(day),
          onClick: () => pick(day),
          role: "gridcell",
          tabIndex: day === focus ? 0 : -1,
          type: "button",
          children: Number(day.slice(8))
        },
        day
      )) }, week[0])) }),
      /* @__PURE__ */ (0, import_jsx_runtime9.jsxs)("div", { className: "date-picker-foot", children: [
        /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("button", { className: "btn link", onClick: () => pick(""), type: "button", children: datePickerLabel.clear }),
        /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("button", { className: "btn h30", disabled: outOfRange(today), onClick: () => pick(today), type: "button", children: datePickerLabel.today })
      ] })
    ] });
  }
  function DatePicker({
    value,
    onChange,
    min,
    max,
    id,
    label
  }) {
    return /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(
      Popover,
      {
        label,
        trigger: ({ props }) => /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("button", { ...props, "aria-label": `${label} ${datePickerLabel.open}`, className: "btn h30 ghost date-picker-trigger", id, children: /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(Icon, { name: "calendar", size: 14 }) }),
        width: 280,
        children: (close) => /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(DatePickerPanel, { close, max, min, onChange, value })
      }
    );
  }

  // frontend/src/MinWidthNotice.tsx
  init_define_import_meta_env();
  var import_jsx_runtime10 = __toESM(require_react_shim(), 1);
  function MinWidthNotice() {
    return /* @__PURE__ */ (0, import_jsx_runtime10.jsxs)("div", { className: "min-width-notice", role: "alert", children: [
      /* @__PURE__ */ (0, import_jsx_runtime10.jsx)(Icon, { name: "alert", size: 20 }),
      /* @__PURE__ */ (0, import_jsx_runtime10.jsx)("b", { children: minWidthNotice.title }),
      /* @__PURE__ */ (0, import_jsx_runtime10.jsx)("p", { children: minWidthNotice.description })
    ] });
  }

  // frontend/src/WorkViews.tsx
  init_define_import_meta_env();
  var import_react6 = __toESM(require_react_shim(), 1);

  // frontend/src/WorkModals.tsx
  init_define_import_meta_env();
  var import_react5 = __toESM(require_react_shim(), 1);

  // frontend/src/idempotency.ts
  init_define_import_meta_env();

  // frontend/src/api.ts
  init_define_import_meta_env();

  // frontend/src/WorkModals.tsx
  var import_jsx_runtime11 = __toESM(require_react_shim(), 1);

  // frontend/src/WorkViews.tsx
  var import_jsx_runtime12 = __toESM(require_react_shim(), 1);
  function taskSpan(task) {
    const start = task.start_date ?? task.due_date ?? null;
    const end = task.due_date ?? task.start_date ?? null;
    if (!start || !end) return null;
    return { start, end: end < start ? start : end };
  }
  function weekSegments(tasks, days, maxLanes) {
    const weekStart = days[0];
    const weekEnd = days[days.length - 1];
    const placed = [];
    const hiddenByDay = {};
    const candidates = tasks.map((task) => ({ task, span: taskSpan(task) })).filter((row) => row.span !== null).filter((row) => row.span.start <= weekEnd && row.span.end >= weekStart);
    const lanes = [];
    for (const { task, span } of candidates) {
      const from = span.start < weekStart ? weekStart : span.start;
      const to = span.end > weekEnd ? weekEnd : span.end;
      const column = days.indexOf(from) + 1;
      const length = days.indexOf(to) - days.indexOf(from) + 1;
      let lane = lanes.findIndex((occupiedUntil) => occupiedUntil === null || occupiedUntil < from);
      if (lane === -1) {
        lane = lanes.length;
        lanes.push(null);
      }
      if (lane >= maxLanes) {
        for (let offset = 0; offset < length; offset += 1) {
          const day = days[column - 1 + offset];
          hiddenByDay[day] = (hiddenByDay[day] ?? 0) + 1;
        }
        continue;
      }
      lanes[lane] = to;
      placed.push({
        task,
        column,
        length,
        lane,
        continuesBefore: span.start < weekStart,
        continuesAfter: span.end > weekEnd,
        span
      });
    }
    return { segments: placed, hiddenByDay };
  }
  function segmentLabel(segment) {
    const { span, task } = segment;
    const dates = span.start === span.end ? task.due_date && !task.start_date ? `${formatDate(span.start)} 기한` : `${formatDate(span.start)} 시작` : `${formatDate(span.start)} – ${formatDate(span.end)}`;
    return `${task.title} \xB7 ${dates} \xB7 ${taskStateLabel[task.state]}`;
  }
  function TaskCalendar({
    tasks,
    onOpen,
    mode = "month",
    onModeChange,
    anchorDate
  }) {
    const today = seoulToday();
    const [anchor, setAnchor] = (0, import_react6.useState)(anchorDate ?? today);
    const [year, month] = anchor.slice(0, 7).split("-").map(Number);
    const cursor = anchor.slice(0, 7);
    const first = `${cursor}-01`;
    const firstWeekday = new Date(Date.UTC(year, month - 1, 1)).getUTCDay();
    const anchorWeekday = new Date(Date.UTC(year, month - 1, Number(anchor.slice(8)))).getUTCDay();
    const gridStart = mode === "week" ? addDays(anchor, -anchorWeekday) : addDays(first, -firstWeekday);
    const days = Array.from({ length: mode === "week" ? 7 : 42 }, (_, index) => addDays(gridStart, index));
    const maxLanes = mode === "week" ? 8 : 3;
    const weeks = (0, import_react6.useMemo)(() => {
      const rows = [];
      for (let index = 0; index < days.length; index += 7) rows.push(days.slice(index, index + 7));
      return rows.map((week) => ({ days: week, ...weekSegments(tasks, week, maxLanes) }));
    }, [tasks, days.join(","), maxLanes]);
    const shift = (delta) => {
      if (mode === "week") {
        setAnchor(addDays(anchor, delta * 7));
        return;
      }
      const date = new Date(Date.UTC(year, month - 1 + delta, 1));
      setAnchor(date.toISOString().slice(0, 10));
    };
    const rangeLabel = mode === "week" ? `${formatDate(days[0])} – ${formatDate(days[6])}` : formatMonth(year, month);
    return /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)("div", { className: "calendar", children: [
      /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)("div", { className: "calendar-toolbar", children: [
        /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)("div", { className: "stepper", children: [
          /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("button", { "aria-label": mode === "week" ? "이전 주" : "이전 달", className: "btn h30 icon", onClick: () => shift(-1), type: "button", children: "‹" }),
          /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("b", { children: rangeLabel }),
          /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("button", { "aria-label": mode === "week" ? "다음 주" : "다음 달", className: "btn h30 icon", onClick: () => shift(1), type: "button", children: "›" })
        ] }),
        /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)("div", { className: "toolbar-group", children: [
          onModeChange && /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)("div", { "aria-label": "캘린더 보기", className: "segmented", role: "tablist", children: [
            /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("button", { "aria-selected": mode === "week", onClick: () => onModeChange("week"), role: "tab", type: "button", children: "주" }),
            /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("button", { "aria-selected": mode === "month", onClick: () => onModeChange("month"), role: "tab", type: "button", children: "월" })
          ] }),
          /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("button", { className: "btn h30", onClick: () => setAnchor(today), type: "button", children: "오늘" })
        ] })
      ] }),
      /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("div", { className: "calendar-weekdays", children: ["일", "월", "화", "수", "목", "금", "토"].map((label) => /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("span", { children: label }, label)) }),
      /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("div", { "aria-label": "업무 캘린더", className: mode === "week" ? "calendar-grid week" : "calendar-grid", role: "grid", children: weeks.map((week) => /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)("div", { className: "calendar-week", children: [
        /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("div", { className: "calendar-days", children: week.days.map((day) => {
          const inMonth = mode === "week" || day.startsWith(cursor);
          const hidden = inMonth ? week.hiddenByDay[day] ?? 0 : 0;
          return /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)(
            "div",
            {
              className: ["calendar-cell", inMonth ? "" : "outside", day === today ? "today" : ""].filter(Boolean).join(" "),
              role: "gridcell",
              children: [
                /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("span", { className: "calendar-day", children: Number(day.slice(8)) }),
                hidden > 0 && /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)("span", { className: "calendar-more", children: [
                  "+",
                  hidden,
                  "개 더"
                ] })
              ]
            },
            day
          );
        }) }),
        /* @__PURE__ */ (0, import_jsx_runtime12.jsx)("div", { className: "calendar-bars", children: week.segments.filter((segment) => mode === "week" || week.days[segment.column - 1].startsWith(cursor) || segment.length > 1).map((segment) => /* @__PURE__ */ (0, import_jsx_runtime12.jsxs)(
          "button",
          {
            "aria-label": segmentLabel(segment),
            className: [
              "calendar-chip",
              segment.task.state,
              segment.continuesBefore ? "continues-before" : "",
              segment.continuesAfter ? "continues-after" : ""
            ].filter(Boolean).join(" "),
            onClick: () => onOpen(segment.task),
            style: { gridColumn: `${segment.column} / span ${segment.length}`, gridRow: segment.lane + 1 },
            title: segmentLabel(segment),
            type: "button",
            children: [
              segment.continuesBefore ? "‹ " : "",
              segment.task.title,
              segment.continuesAfter ? " ›" : ""
            ]
          },
          `${segment.task.task_id}-${segment.column}`
        )) })
      ] }, week.days[0])) })
    ] });
  }
  return __toCommonJS(ds_entry_exports);
})();
window.SCAX=SCAX.__dsMainNs?Object.assign({},SCAX,SCAX.__dsMainNs,{__dsMainNs:undefined}):SCAX;
