
let mainPath = '../ProyectoIntegrador/Grafistica/apps/';

module.exports = {
    entry: {
        importdata:mainPath+'viewer/static/apps/import.js',
    },
    output: {
        filename: '[name].js',
        path: __dirname + '/Grafistica/static/dist_g/bundle'
    },
    resolve: {
        alias: {
            // 'vue$': 'vue/dist/vue.esm.js',
            'vue': 'vue/dist/vue.min.js'
        },
        extensions: ['*', '.js', '.vue', '.json']
      }
};