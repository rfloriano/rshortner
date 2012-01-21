function Shortener(id_form, id_table, id_errors, opts){
    var self = this;

    var default_options = {
        id_url: "id_url",
        id_short: "id_short"
    }
    self.options = $.extend(default_options, opts);

    self.fields = {};
    self.ul_errors = "ul_errors";

    self.__init__ = function(id_form, id_table, id_errors){
        self.form = $("#"+id_form);
        self.table = $("#"+id_table);
        self.errors = $("#"+id_errors);

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
        self._clearErrors();
        self.clear_url();
        var order = ["url", "short_url", "created_at", "page_view"];
        td = "<tr>";
        for (o in order){
            if (order[o] == "short_url"){
                td += '<td><a href="'+data[order[o]]+'">'+ data[order[o]] +'</a></td>';
                self.fields.short.val(data[order[o]]);
            }else{
                td += "<td>"+data[order[o]]+"</td>";
            }
        }
        td += "</tr>";
        self.table.prepend(td);
        self.table.find("#default-message").remove();
        self.fields.short.select();
    }

    self._clearErrors = function(){
        $("#"+self.ul_errors).remove();
        self.errors.removeClass("alert-message block-message error");
    }

    self._markErrors = function(data){
        var li = "";
        for (error in data.errors.url){
            li += "<li>"+ data.errors.url[error] +"</li>";
        }
        self._markError(li);
    }

    self._markError = function(li){
        self._clearErrors();
        $ul = $('<ul id="'+ self.ul_errors +'"/>');
        $ul.append(li);
        self.errors.prepend($ul);
        self.errors.addClass("alert-message block-message error");
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
                }
                else if (data.short_url == ""
                     &&  data.errors.url.length > 0
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

    return self.__init__(id_form, id_table, id_errors);
}

$(document).ready(function(){
    shortener = new Shortener("id_form_shortener", "table_list_url", "url_errors");
});