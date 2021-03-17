const mongoose = require('mongoose');

const TranslationSchema = mongoose.Schema({
    code: String,
    name: String
}, {
    timestamps: true
});

module.exports = mongoose.model('Translations', TranslationSchema);
