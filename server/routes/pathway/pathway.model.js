const mongoose = require('mongoose');

const PathwaySchema = mongoose.Schema({
    name: String,
    file: Object,//{type: String, data: String},
    graph: Object,
    image: Object//{type: String, data: String} Buffer
}, {
    timestamps: true
});

module.exports = mongoose.model('Pathways', PathwaySchema);
