import { Component, OnInit } from '@angular/core';
import {HomepageService} from "../homepage.service";

@Component({
  selector: 'app-graph-maker',
  templateUrl: './graph-maker.component.html',
  styleUrls: ['./graph-maker.component.css']
})
export class GraphMakerComponent implements OnInit {

  constructor(private service: HomepageService) { }

  currentGraph: any;
  currentNodes: any[];
  currentEdges: any[];
  fromNode: string;
  toNode: string;
  graphName: string;

  ngOnInit() {
    this.currentGraph = {};
    this.currentNodes = [];
    this.currentEdges = [];
  }

  addNode(){
    const elem = (<HTMLInputElement>document.getElementById("node-input"));
    const node = elem.value;
    elem.value = "";
    // TODO check for duplicated nodes in current array
    this.currentNodes.push({"name":node});//, "index": this.currentNodes.length});
  }

  deleteNode(node){
    this.currentNodes = this.currentNodes.filter(function(value, index, arr){
      return value != node;
    });
    let key;
    for(key in this.currentGraph){
      if(this.currentGraph[key].includes(node.name)){
        this.currentGraph[key] = this.currentGraph[key].filter(function(value, index, arr){
          return value != node.name;
        });
      }
      if(this.currentGraph.hasOwnProperty(key) && key == node.name){
        console.log("Deleting key");
        delete this.currentGraph[key];
      }
    }
    //this.updateIndexOfNodes();
  }

  addEdge(){
    console.log("Adding relation");
    console.log("From Node");
    console.log(this.fromNode);
    console.log("To Node");
    console.log(this.toNode);
    if (this.fromNode === this.toNode)
      alert("Cannot add relation to same node");
    else {
      if (this.currentGraph[this.fromNode]) {
        this.currentGraph[this.fromNode].push(this.toNode);
      } else {
        this.currentGraph[this.fromNode] = [this.toNode];
      }
      this.currentEdges.push({'from':this.fromNode, 'to': this.toNode});
      console.log("Current graph:");
      console.log(this.currentGraph)
    }
  }

  deleteEdge(edge){
    this.currentEdges = this.currentEdges.filter(function(value, index, arr){
      return value != edge;
    });

    this.currentGraph[edge.from] = this.currentGraph[edge.from].filter(function(value, index, arr){
      return value != edge.to;
    });
    console.log("Current graph:");
    console.log(this.currentGraph)
  }

  setFromNode(node){
    console.log("Set From Node");
    console.log(node);
    this.fromNode = node.target.value;
  }

  setToNode(node){
    this.toNode = node.target.value;
  }

  saveGraph(){
    const elem = (<HTMLInputElement>document.getElementById("graph-name"));
    this.graphName = elem.value;
    if(this.graphName !== ""){
      //alert("Now connect to service");
      this.service.setCurrentGraph1(JSON.stringify(this.currentGraph), this.graphName, "Manual Definition");
    }else{
      alert("Graph name cannot be empty");
    }
  }

  /*updateIndexOfNodes(){ // Unused now
    let i = 0;
    for(i; i< this.currentNodes.length; i++){
      this.currentNodes[i]['index'] = i;
    }
  }*/

}
