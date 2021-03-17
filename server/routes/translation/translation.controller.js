const Translation = require('./translation.model.js');


//Create new Translation
exports.create = (req, res) => {
    // Request validation
    if(!req.body) {
      console.log("X0");
        return res.status(400).send({
            message: "Translation content can not be empty"
        });
    }
    // Create a Translation
    const translation = new Translation({
        name: req.body.name || "Na name provided",
        code: req.body.code || "No code provided"
    });

    // Save Translation in the database
    translation.save()
    .then(data => {
        res.send(data);
    }).catch(err => {
        res.status(500).send({
            message: err.message || "Something wrong while creating the translation."
        });
    });
};

// Retrieve all translations from the database.
exports.findAll = (req, res) => {
  console.log("Hello there");
  Translation.find()
    .then(translations => {
        res.send(translations);
    }).catch(err => {
        res.status(500).send({
            message: err.message || "Something wrong while retrieving translations."
        });
    });
};

// Find a single translation with a translationId
exports.findOne = (req, res) => {
    Translation.findById(req.params.translationId)
    .then(translation => {
        if(!translation) {
            return res.status(404).send({
                message: "Translation not found with id " + req.params.translationId
            });            
        }
        res.send(translation);
    }).catch(err => {
        if(err.kind === 'ObjectId') {
            return res.status(404).send({
                message: "Translation not found with id " + req.params.translationId
            });                
        }
        return res.status(500).send({
            message: "Something wrong while retrieving translation with id " + req.params.translationId
        });
    });
};

// Update a translation
exports.update = (req, res) => {
    // Validate Request
    if(!req.body) {
        return res.status(400).send({
            message: "Translation content can not be empty"
        });
    }

    // Find and update translation with the request body
    Translation.findOneAndUpdate(req.params.translationId, {
        name: req.body.name || "No name provided",
      code: req.body.code || "No code provided"
    }, {new: true})
    .then(translation => {
        if(!translation) {
            return res.status(404).send({
                message: "Translation not found with id " + req.params.translationId
            });
        }
        res.send(translation);
    }).catch(err => {
        if(err.kind === 'ObjectId') {
            return res.status(404).send({
                message: "Translation not found with id " + req.params.translationId
            });                
        }
        return res.status(500).send({
            message: "Something wrong updating translation with id " + req.params.translationId
        });
    });
};

// Delete a translation with the specified translationId in the request
exports.delete = (req, res) => {
    Translation.findOneAndDelete(req.params.translationId)
    .then(pathway => {
        if(!pathway) {
            return res.status(404).send({
                message: "Translation not found with id " + req.params.translationId
            });
        }
        res.send({message: "Translation deleted successfully!"});
    }).catch(err => {
        if(err.kind === 'ObjectId' || err.name === 'NotFound') {
            return res.status(404).send({
                message: "Translation not found with id " + req.params.translationId
            });                
        }
        return res.status(500).send({
            message: "Could not delete translation with id " + req.params.translationId
        });
    });
};
