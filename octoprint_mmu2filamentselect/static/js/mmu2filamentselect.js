(function (global, factory) {
    if (typeof define === "function" && define.amd) {
        define(["OctoPrintClient"], factory);
    } else {
        factory(global.OctoPrintClient);
    }
})(this, function(OctoPrintClient) {
    var OctoPrintMMU2Select = function(base) {
        this.base = base;
    };

    OctoPrintMMU2Select.prototype.select = function(index, opts) {
        var data = {
            choice: index
        };
        return this.base.simpleApiCommand("mmu2filamentselect", "select", data, opts);
    };

    OctoPrintClient.registerPluginComponent("mmu2filamentselect", OctoPrintMMU2Select);
    return OctoPrintMMU2Select;
});

$(function() {
    function MMU2SelectViewModel(parameters) {
        var self = this;

        self.settings = parameters[0];
        self.loginState = parameters[1];

        self._modal = undefined;

        self._showPrompt = function() {
            var opts = {
                title: gettext("Prusa MMU2 filament select"),
                message: gettext("Select the filament spool you wish to use for this single color print."), 
                selections: {0:"Filament 1",1:"Filament 2",2:"Filament 3",3:"Filament 4",4:"Filament 5"},
                onselect: function(index) {
                    if (index > -1) {
                        self._select(index);
                    }
                },
                onclose: function() {
                    self._modal = undefined;
                }
            };

            self._modal = showSelectionDialog(opts)
            setTimeout(self._closePrompt, self.settings.settings.plugins.mmu2filamentselect.timeout() * 1000);
        };

        self._select = function(index) {
            OctoPrint.plugins.mmu2filamentselect.select(index);
        };

        self._closePrompt = function() {
            if (self._modal) {
                self._modal.modal("hide");
            }
        };

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (!self.loginState.isUser()) return;
            if (plugin !== "mmu2filamentselect") {
                return;
            }

            switch (data.action) {
                case "show": {
                    self._showPrompt();
                    break;
                }
                case "close": {
                    self._closePrompt();
                    break;
                }
            }
        }

    }

    OCTOPRINT_VIEWMODELS.push({
        construct: MMU2SelectViewModel,
        dependencies: ["settingsViewModel","loginStateViewModel"]
    });
});