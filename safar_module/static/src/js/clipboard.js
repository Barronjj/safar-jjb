odoo.define('safar_module.Recupclipboard', function(require) {
    "use strict";

    var Widget = require('web.Widget');
    var registry = require('web.widget_registry');

    var core = require('web.core');
    var QWeb = core.qweb;

    var PasteConfig = Widget.extend({

        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.id = params.res_id
        },

        start: function () {
            this.$widget = $(QWeb.render('copy_btn_template'));
            this.$copyLink = this.$widget.find('.copy_btn');
            this.$widget.appendTo(this.$el);
            this.$copyLink.click(this.coller_config.bind(this));
        },

        coller_config: function () {
            navigator.clipboard.readText()
            .then(clipText => {
                const el = document.activeElement;
                document.getElementsByName("s_configuration")[0].value = clipText;
                console.log(clipText)
                console.log(this.red_id);

//                this._rpc({
//                    model: 'sale.order.line',
//                    method: 'paste_config',
//                    args: [[this.id], clipText],
//                    })
//                    .then(function (p) {
//
//                })
            });
        },
    })

    registry.add('paste-config', PasteConfig);

    return PasteConfig;

});

//odoo.define('safar_module.Recupclipboard', function(require) {
//    "use strict";
//
//    var Widget = require('web.Widget');
//    var registry = require('web.widget_registry');
//    var core = require('web.core');
//    var QWeb = core.qweb;
//
//    var PasteConfig = Widget.extend({
//        start: function () {
//            this.$widget = $(QWeb.render('copy_btn_template'));
//            this.$copyLink = this.$widget.find('.copy_btn');
//            this.$widget.appendTo(this.$el);
//            this.$copyLink.click(this.coller_config.bind(this));
//        },
//
//        coller_config: function () {
//            navigator.clipboard.readText()
//                .then(clipText => {
//                    const el = document.activeElement;
//
//            //console.log(clipText)
//            //document.getElementsByName("s_configuration")[0].value = clipText;
//            //call_rpc(clipText)
//
//            var _this = this;
//            var rpc = require('web.rpc')
//
//            return this._rpc({
//                    model: 'sale.order.line',
//                    method: 'paste_config',
//                    args: [[],[clipText]],
//                })
//                .then(function (p) {
//
//                   })
//            });
//        },
//
////        coller_config: function () {
////            navigator.clipboard.readText()
////                .then(clipText => {
////                    const el = document.activeElement;
////            console.log(clipText)
////            document.getElementsByName("s_configuration")[0].value = clipText;
////            })
////        },
//
////        call_rpc: function (maconfig) {
////
////        },
//    })
//
//    registry.add('paste-config', PasteConfig);
//
//    return PasteConfig;
//});

//odoo.define('safar_module.Recupclipboard', function(require) {
//    "use strict";
//
//        var Widget = require('web.Widget');
//        var registry = require('web.field_registry');
//        var PasteConfig = Widget.extend({
//            events: {
//                "click button[name='click_me']": "coller_config",
//            },
//
//            coller_config: function () {
//                navigator.clipboard.readText()
//                   .then(clipText => {
//                     const el = document.activeElement;
//                document.getElementsByName("s_configuration")[0].value = clipText;
//                })
//            },
//
//    //        call_rpc: function (maconfig) {
//    //
//    //        },
//        })
//
//        registry.add('paste-config', PasteConfig);
//
//        return PasteConfig;
//    });


//odoo.define('safar_module.Recupclipboard', function(require) {
//"use strict";
//
//    var Widget = require('web.Widget');
//
//    var registry = require('web.field_registry');
//
//    var PasteConfig = Widget.extend({
//        events: {
//            "click button[name='click_me']": "coller_config",
////             "click #id_click_me": "coller_config"
//            },
//
//        coller_config: function () {
//            navigator.clipboard.readText()
//               .then(clipText => {
//                 const el = document.activeElement;
//            document.getElementsByName("s_configuration")[0].value = clipText;
//            })
//        },
//
////        call_rpc: function (maconfig) {
////
////        },
//    })
//
//    registry.add('paste-config', PasteConfig);
//
//    return PasteConfig;
//});

//odoo.define('safar_module.Recup_clipboard', function (require) {
//"use strict";
//
//    var Widget = require('web.Widget');
//
//    var AttachmentBox = Widget.extend({
//    template: 'mail.chatter.AttachmentBox',
//    events: {
//        "click .o_attachment_download": "_onAttachmentDownload",
//        "click .o_attachment_view": "_onAttachmentView",
//        "click .o_attachment_delete_cross": "_onDeleteAttachment",
//        "click .o_upload_attachments_button": "_onUploadAttachments",
//        "change .o_chatter_attachment_form .o_form_binary_form": "_onAddAttachment",
//    },
//
//    function coller_config() {
//     navigator.clipboard.readText()
//       .then(clipText => {
//         const el = document.activeElement;
//    //       if (el.nodeName === 'INPUT') {
//    //         const newCursorPos = el.selectionStart + clipText.length;
//    //         el.value =
//    //           el.value.substring(0, el.selectionStart) +
//    //           clipText +
//    //           el.value.substring(el.selectionEnd);
//    //         el.setSelectionRange(newCursorPos, newCursorPos);
//    //         alert('value1=' + el.value);
//    //       }
//         //alert(clipText);
//         //document.getElementsByName("s_configuration")[0].value = clipText;
//    //      document.getElementsByName("s_configuration")[0].val('clipText');
//    //      document.getElementsByName("s_configuration")[0].text('clipText')';
//         call_rpc('cliptext');
//       });
//    },
//
//// odoo.define('auth_password_policy.ChangePassword', function (require) {
//// "use strict";
//
//
//    function call_rpc(maconfig) {
//        var _this = this;
//        var rpc = require('web.rpc')
//        var getPolicy = this._rpc({
//            model: 'sale.order.line',
//            method: 'paste_config',
//            args: ['maconfig']
//        }).then(function (p) {
//    //         _this._meter = new Meter(_this, new policy.Policy(p), policy.recommendations);
//        });
//    },
//});


// odoo.define('safar_module.Maconfig', function (require) {
//     "use strict";

// //     var core = require('web.core');
//     var Widget = require('web.Widget');
// //     var QWeb = core.qweb;
// //     var _t = core._t;

//     var Maconfig = Widget.extend({
// //         template: 'mail.chatter.AttachmentBox',
//         events: {
//             "click button[name='click_me']"; "_onClickButton",
//         },


//         _onClickButton: function (ev) {
//                 navigator.clipboard.readText()
//                     .then(clipText => {
//                         const el = document.activeElement;
//     //            document.getElementsByName("s_configuration")[0].val('clipText');
//                 });
//                 ev.paste_config(clipText);
//             },
//     });
// });

// odoo.define('safar_module.recup_clipboard', function (require){
//     "use strict";
//     var form_widget = require('web.form_widgets');
//     var core = require('web.core');
//     var _t = core._t;
//     var QWeb = core.qweb;

//     form_widget.WidgetButton.include({
//         on_click: function() {
//              if(this.node.attrs.custom === "click_me"){

//                 alert("It works!!");
//                  navigator.clipboard.readText()
//        .then(clipText => {
//          const el = document.activeElement;
//                      document.getElementsByName("s_configuration")[0].value = clipText;

//                 return;
//              }
//              this._super();
//         },
//     });
//     });