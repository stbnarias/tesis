module.exports = (router) => {
    const translations = require('./translation.controller.js');

    // Create a new Pathway
    router.post('/translations', translations.create);

    // Retrieve all Pathways
    router.get('/translations', translations.findAll);

    // Retrieve a single Pathway with pathwayId
    router.get('/translations/:translationId', translations.findOne);

    // Update a Pathway with pathwayId
    router.put('/translations/:translationId', translations.update);

    // Delete a Pathway with pathwayId
    router.delete('/translations/:translationId', translations.delete);
}
