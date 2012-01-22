function Shortener(id_form, id_table, messages, opts){
    var self = this;

    var default_options = {
        id_url: "id_url",
        id_short: "id_short",
        errors_class: "alert-message block-message error",
        success_class: "alert-message block-message success",
        remove_too: null,
        can_add_rows: false
    }
    self.options = $.extend(default_options, opts);

    self.fields = {};
    self.ul_errors = "ul_errors";
    self.ul_success = "ul_success";
    self_short_url = "short_url";
    self._order = ["url", self_short_url, "created_at", "page_view", "details"];

    self.__init__ = function(id_form, id_table, messages){
        self.form = $("#"+id_form);
        self.table = $("#"+id_table);
        self.messages = $("#"+messages);

        self._getFieldsFromForm();
        self._bind_events();
        self.clear();
    }

    self._bind_events = function(){
        self.form.submit(self.submit);
    }

    self._getFieldsFromForm = function(){
        self.fields.url = self.form.find("#"+self.options.id_url);
        self.fields.short = self.form.find("#"+self.options.id_short);
    }

    self._addTableRow = function(data){
        if (!self.options.can_add_rows){
            return null;
        };
        self._clearMessages();
        self.clear_url();
        td = "<tr>";
        for (o in self._order){
            if (self._order[o] == "short_url"){
                td += '<td><a href="'+data[self._order[o]]+'">'+ data[self._order[o]] +'</a></td>';
            }else if (self._order[o] == "details"){
                td += '<td><a href="'+data[self._order[o]]+'">Detalhes</a></td>';
            }else{
                td += "<td>"+data[self._order[o]]+"</td>";
            }
        }
        td += "</tr>";
        self.table.prepend(td);
        self.table.find("#default-message").remove();
        if (self.options.remove_too){
            $("."+ self.options.remove_too).remove();
        }
    }

    self._clearErrors = function(){
        $("#"+self.ul_errors).remove();
        self.messages.removeClass(self.options.errors_class);
    }

    self._markErrors = function(data){
        var li = "";
        for (error in data.errors.url){
            li += "<li>"+ data.errors.url[error] +"</li>";
        }
        self._markError(li);
    }

    self._markError = function(li){
        self._clearMessages();
        $ul = $('<ul id="'+ self.ul_errors +'"/>');
        $ul.append(li);
        self.messages.prepend($ul);
        self.messages.addClass(self.options.errors_class);
    }

    self._clearSuccess = function(){
        $("#"+self.ul_success).remove();
        self.messages.removeClass(self.options.success_class);
    }

    self._markSuccess = function(li){
        self._clearMessages();
        $ul = $('<ul id="'+ self.ul_success +'"/>');
        $ul.append(li);
        self.messages.prepend($ul);
        self.messages.addClass(self.options.success_class);
    }

    self._clearMessages = function(){
        self._clearErrors();
        self._clearSuccess();
    }

    self._selectShortenerUrl = function(data){
        self.fields.short.val(data[self_short_url]);
        self.fields.short.select();
    }

    self.clear = function(){
        self.clear_url();
        self.clear_short();
    }

    self.clear_url = function(){
        self.fields.url.val("");
    }

    self.clear_short = function(){
        self.fields.short.val("");
    }

    self.submit = function(){
        $.ajax({
            type: 'POST',
            dataType: 'json',
            url: self.form.attr("action"),
            data: self.form.serialize(),
            success: function(data){
                self.clear_url();
                if (data.created){
                    self._addTableRow(data);
                    self._selectShortenerUrl(data);
                    message = "<li>URL criada com sucesso! Você pode pressionar ctrl+c para copiar a sua URL"
                    if (!self.options.can_add_rows){
                        message += " e acompanhar as estatísicas abaixo."
                    };
                    message += "</li>"
                    self._markSuccess(message);
                }else if (data.short_url){
                    self._selectShortenerUrl(data);
                    message = "<li>Esta URL já existia em nosso banco de dados. Nós a encontramos para você. Você pode pressionar ctrl+c para copiar a sua URL"
                    if (!self.options.can_add_rows){
                        message += " e acompanhar as estatísicas abaixo."
                    };
                    message += "</li>"
                    self._markSuccess(message);
                }
                else if (data.errors.url.length > 0
                ){
                    self._markErrors(data);
                }
            },
            error: function(data){
                self.clear_short();
                self._markError("<li>Você precisa enviar uma URL para encurtar</li>");
            }
        });
        return false;
    }

    return self.__init__(id_form, id_table, messages);
}

$(document).ready(function(){
    shortener = new Shortener(
        "id_form_shortener", 
        "table_list_url", 
        "messages", 
        {
            can_add_rows: can_add_rows, 
            remove_too: "data_not_find"
        }
    );
});

