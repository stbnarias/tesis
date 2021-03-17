import { Component, OnInit } from '@angular/core';
import * as $ from 'jquery';
import {FormBuilder, FormGroup} from "@angular/forms";
import { HomepageService } from '../homepage.service';

@Component({
  selector: 'app-algorithm-selector',
  templateUrl: './algorithm-selector.component.html',
  styleUrls: ['./algorithm-selector.component.css']
})
export class AlgorithmSelectorComponent implements OnInit {

  constructor(private service: HomepageService) {}

  options: any[];
  currentOption: string;

  ngOnInit() {
    $(document).ready( function() {
      $("#filter-bar li").click(function(){
        $("#filter-bar li").removeClass("active");
        $(this).addClass("active");
        $("#filter-bar").removeClass().addClass($(this).attr("data-target"));
      });
    });

    this.options = [{value: 'A1', label:'2D to 1D Transformation'}, {value: 'A2', label:'Differentiation by pairs'}];
    this.currentOption = 'Original';
    //this.service.setCurrentAlgorithmCode('A1');
  }

  changeAlgorithmView(currentView: string) {
    //alert(currentView);
    if(currentView === 'Original'){
      this.options = [{value: 'A1', label:'2D to 1D Transformation'}, {value: 'A2', label:'Differentiation by pairs'}];
    }else{
      if (currentView === 'Extended'){
        this.options = [{value: 'A1T1', label: '1.1 - Starting at any node, Finishing at any node'},
                        {value: 'A1T2', label: '1.2 - Starting at a given node, Finishing at any node'},
                        {value: 'A1T3', label: '1.3 - Starting at a given node, Finishing at a given node'},
                        {value: 'A1T4', label: '1.4 - Evaluation of all possible paths'},
                        {value: 'A1T5', label: '1.5 - Starting at any node, Finishing at a given node'}];
      }else{
        this.options = [{value: 'A3', label: "Not available yet"}];
      }
    }
    this.service.setCurrentAlgorithmCode(this.options[0]['value']); // for parent change
    this.setCurrentAlgorithmTypeSelected(currentView);
  }

  displayCurrentValue(value: string){
    //alert('Current value: ' + value);
    this.service.setCurrentAlgorithmCode(value); // for child change
  }

  /*showNodeParametersView(){
    let view = document.getElementById("Nodes-Parameter-View");
    view.setAttribute("style", "visibility: visible");
    //document.getElementById("Nodes-Parameter-View").style.transform = "visibility: visible;";
  }

  hideNodeParametersView(){
    let view = document.getElementById("Nodes-Parameter-View");
    view.setAttribute("style", "visibility: hidden;");
    //document.getElementById("Nodes-Parameter-View").style.transform = "visibility: hidden;";
  }*/

  setCurrentAlgorithmTypeSelected(type: string){
    this.service.setCurrentAlgorithmType(type);
  }




}
