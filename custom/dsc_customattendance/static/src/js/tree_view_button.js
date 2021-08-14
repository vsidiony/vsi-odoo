odoo.define('tree_menu.tree_view_button', function (require){
    "use strict";
    
    var core = require('web.core');
    var ListView = require('web.ListView');
    var QWeb = core.qweb;
    
    // ListView.include({
    //     render_buttons: function() {
    //         console.log("Render Function");    
    //         // GET BUTTON REFERENCE
    //         this._super.apply(this, arguments)
    //         if (this.$buttons) {
    //             console.log("Button Found");  
    //             var btn = this.$buttons.find('.copy_from_attendance')
    //         }
    
    //         // PERFORM THE ACTION
    //         btn.on('click', this.proxy('do_new_button'))
    
    //     },
    //     do_new_button: function() {
    //         console.log("Click Function");    
    //         instance.web.Model('dsc.attendance')
    //             .call('action_copy_from_attendance', [[]])
    //             .done(function(result) {
    //                 // < do your stuff, if you don't need to do anything remove the 'done' function >
    //             })
    //         }
    // })    

    ListView.include({
        render_buttons: function() {
            console.log("Render Function");       
            // GET BUTTON REFERENCE
            this._super.apply(this, arguments)
            if (this.$buttons) {
                var btn = this.$buttons.find('.copy_from_attendance')
                console.log(btn);
            }

            // PERFORM THE ACTION
            btn.on('click', this.proxy('do_new_button'))
    
        },
        do_new_button: function() {
            var self = this;
            var model = new instance.web.Model("dsc.attendance");
            model.call("action_copy_from_attendance",[[]]);            
        }
    });  

    // ListView.include({       

    //     render_buttons: function($node) {
    //             var self = this;
    //             this._super($node);
    //             this.$buttons.find('.copy_from_attendance').click(this.proxy('tree_view_action'));
    //             alert("Test Initialization");
    //     },

    //     tree_view_action: function () {
    //         alert("Test Working");
    //         var self = this;
    //         var model = new instance.web.Model("dsc.attendance");
    //         model.call("action_copy_from_attendance",[[]]);  

    //     } 

    // });

});