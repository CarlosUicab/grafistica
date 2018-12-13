import Vue from 'vue'
var _ = require('lodash');


_.each([12,34],function (o) {
    console.log(o)
})
let vue = new Vue({
    el: "#app",
    data: {
        data_json:  Object.assign({}, my_json),
        data_origin:my_json,
        columns: {},
        json: {},
        filteractive:false,
        datafilter:'', // lo que el usuario escribe en el filtro
        filtersnumber:'=',
        filterstext:'=',
        empty:false,
        filter:{
            name:'',
            type:''
        }
    },
    mounted: function () {
    },
    methods: {
        removeAllFilter:function(){
            this.data_json= Object.assign({}, my_json);
            this.filter.name = '';
            this.filter.type=''
        },
        filterdata:function(data){
            /// filtramos usando el dato que esta escirbiendo el usuario con la configuracion del filtro seleccionado
            // this.data_json.data = _.filter(this.data_json.data, function(o) { return o[filter.name]===data; });
            // this.data_json.data = _.head(this.data_json.data)
            let app = this;
            this.data_json.data = _.filter(this.data_json.data, function(obj) {
                if(app.filter.type === 'number'){
                    if(app.empty){
                            return obj[app.filter.name]!==null;
                    }
                    console.log(app.empty)
                    // si es tipo number entonces hay que convertir el dato a numerico para que se pueda filtrar correctamente con los objetos
                    if(app.filtersnumber==='='){
                        return obj[app.filter.name]===Number(data);
                    }else if(app.filtersnumber==='<='){
                        return obj[app.filter.name]<= Number(data);
                    }else if(app.filtersnumber==='>='){
                         return obj[app.filter.name]>=Number(data);
                    }else if(app.filtersnumber==='<>'){
                         return obj[app.filter.name]!==Number(data);
                    }else{
                        return obj[app.filter.name]===Number(data);
                    }

                }else{
                    let obstr = obj[app.filter.name];
                    if(app.empty){
                            return obstr!==null;
                    }

                    if(obstr!==null){
                        obstr = obstr.toLowerCase();
                    }else{
                        obstr="";
                    }

                    let datastr = data.toLowerCase();

                    if(app.filterstext==='='){
                        // es igual
                        return obstr===datastr;
                    }else if(app.filterstext==='*'){
                        // contiene
                        return obstr.includes(datastr);
                    }else if(app.filterstext==='>='){
                        // empieza con
                        return obstr.startsWith(datastr);
                    }else if(app.filterstext==='<>'){
                        if(datastr==='""'){
                            return obstr!==null;
                        }else{
                            return obstr!==datastr;
                        }

                    }




                    return obj[app.filter.name].toLowerCase().startsWith(data.toLowerCase());
                };

            });
            this.filteractive = false;
        },
        filterByColumn:function(name_key,type){
            console.log(name,type);
            this.datafilter = '';
            this.filter.name = name_key;
            this.filter.type = type;
            this.filteractive = true;
        },
        limpiar:function () {
            if(this.empty){
                this.datafilter="";
            }
        },
        changevalue: function (index, key, value) {
            this.data_json.data[index][key] = value;
        },
        deleteItem: function (index) {
            this.data_json.data.splice(index, 1);
        },
        makepost: function () {
            let json = JSON.stringify(this.data_json);
            document.getElementById('jsondata_prev').value = json;
            document.getElementById("frmenviarjson").submit();
        }
    }
});