module.exports = (router) => {
    const pathways = require('./pathway.controller.js');

    // Create a new Pathway
    router.post('/pathways', pathways.create);

    // Retrieve all Pathways
    router.get('/pathways', pathways.findAll);

    // Retrieve a single Pathway with pathwayId
    router.get('/pathways/:pathwayId', pathways.findOne);

    // Update a Pathway with pathwayId
    router.put('/pathways/:pathwayId', pathways.update);

    // Delete a Pathway with pathwayId
    router.delete('/pathways/:pathwayId', pathways.delete);
}
