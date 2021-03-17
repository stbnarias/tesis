const Pathway = require('./pathway.model.js');
const fs = require('fs');

//Create new Pathway
exports.create = (req, res) => {
  // Request validation
  if(!req.body) {
    console.log("X0");
      return res.status(400).send({
          message: "Pathway content can not be empty"
      });
  }

  // Create a Pathway
  // TODO: asignar estas rutas en un solo lugar, como en el main o algo asi
  let file;
  if (req.body.file){
    try{
      file = fs.readFileSync(__dirname + "/../../../temp_uploads/"+req.body.file);
    }catch (e) {
      file = e;
    }
  }
  let image;
  if(req.body.image){
    try{
      image = fs.readFileSync(__dirname + "/../../../images/"+req.body.image);
    }catch (e) {
      image = e;
    }
  }

  const pathway = new Pathway({
      name: req.body.name || "Unnamed pathway",
      file: file || "No file provided", //fs.readFileSync(__dirname + "/../../../temp_uploads/"+req.body.file) || "No file attached", //req.body.file
      graph: req.body.graph || "No graph provided",
      image: image || "No image provided"//fs.readFileSync(__dirname + "/../../../images/"+req.body.image) || "No image included" //req.body.image
  });

  // Save Pathway in the database
  pathway.save()
  .then(data => {
    console.log("X2");
      res.send(data);
  }).catch(err => {
    console.log("X3");
      res.status(500).send({
          message: err.message || "Something wrong while creating the pathway."
      });
  });
  console.log("X4");
};

// Retrieve all pathways from the database.
exports.findAll = (req, res) => {
  Pathway.find()
    .then(pathways => {
        res.send(pathways);
    }).catch(err => {
        res.status(500).send({
            message: err.message || "Something wrong while retrieving pathways."
        });
    });
};

// Find a single pathway with a pathwayId
exports.findOne = (req, res) => {
  Pathway.findById(req.params.pathwayId)
  .then(pathway => {
      if(!pathway) {
          return res.status(404).send({
              message: "Pathway not found with id " + req.params.pathwayId
          });
      }
      res.send(pathway);
  }).catch(err => {
      if(err.kind === 'ObjectId') {
          return res.status(404).send({
              message: "Pathway not found with id " + req.params.pathwayId
          });
      }
      return res.status(500).send({
          message: "Something wrong retrieving pathway with id " + req.params.pathwayId
      });
  });
};

// Update a pathway
exports.update = (req, res) => {
  // Validate Request
  if(!req.body) {
      return res.status(400).send({
          message: "Pathway content can not be empty"
      });
  }

  // Find and update pathway with the request body
  Pathway.findByIdAndUpdate(req.params.pathwayId, {
      name: req.body.name || "No pathway name",
    file: req.body.file || "No file attached",
    graph: req.body.graph || "No graph provided",
    image: req.body.image || "No image included"
  }, {new: true})
  .then(pathway => {
      if(!pathway) {
          return res.status(404).send({
              message: "Pathway not found with id " + req.params.pathwayId
          });
      }
      res.send(pathway);
  }).catch(err => {
      if(err.kind === 'ObjectId') {
          return res.status(404).send({
              message: "Pathway not found with id " + req.params.pathwayId
          });
      }
      return res.status(500).send({
          message: "Something wrong updating pathway with id " + req.params.pathwayId
      });
  });
};

// Delete a pathway with the specified pathwayId in the request
exports.delete = (req, res) => {
  Pathway.findByIdAndRemove(req.params.pathwayId)
  .then(pathway => {
      if(!pathway) {
          return res.status(404).send({
              message: "Pathway not found with id " + req.params.pathwayId
          });
      }
      res.send({message: "Pathway deleted successfully!"});
  }).catch(err => {
      if(err.kind === 'ObjectId' || err.name === 'NotFound') {
          return res.status(404).send({
              message: "Pathway not found with id " + req.params.pathwayId
          });
      }
      return res.status(500).send({
          message: "Could not delete pathway with id " + req.params.pathwayId
      });
  });
};
