odoo.define('openeducat_lms.open-modal', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require("web.Dialog");
    var session = require('web.session');
    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var websiteRootData = require('website.root');
    var utils = require('web.utils');
    var _t = core._t;
    var qweb = core.qweb;

    var OpenModalWidget = Widget.extend({

    events: {

        'click .preview-btn': '_onClickPreviewButton',
    },

    xmlDependencies: ['/openeducat_lms/static/src/xml/openmodal.xml'],
    init: function () {
            this._super.apply(this, arguments);
    },
    start: function (editable_mode) {

    },

    _onClickPreviewButton: function(e){
        var material_id = $(e.currentTarget).data('material-id');
        if (material_id != undefined)
        {
            ajax.jsonRpc('/get/material', 'call',
            {
                'material_id': material_id,
            }).then(function (data) {
                if (data['embed_code'])
                {
                    var embed_code = qweb.render('MaterialDetails',
                    {
                        data: data['embed_code']


                    });
                    $('.modal-title-lms').html(data['name'])
                    $('.modal-body').html(embed_code);
                    $('#preview-modal').modal("show")

                }


                });

        }


    }



})

websiteRootData.websiteRootRegistry.add(OpenModalWidget, '.card-body');


});

