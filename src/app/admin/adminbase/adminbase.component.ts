import { Component, OnInit } from '@angular/core';
import * as $ from "jquery";

@Component({
  selector: 'app-adminbase',
  templateUrl: './adminbase.component.html',
  styleUrls: ['./adminbase.component.css']
})
export class AdminbaseComponent implements OnInit {

  constructor() { }

  filesSelected:boolean;
  dictionarySelected:boolean;

  ngOnInit() {
    $(document).ready( function() {
      $("#filter-bar li").click(function(){
        $("#filter-bar li").removeClass("active");
        $(this).addClass("active");
        $("#filter-bar").removeClass().addClass($(this).attr("data-target"));
      });
    });
    this.filesSelected = true;
    this.dictionarySelected = false;
  }

  switchToFiles(){
    this.filesSelected = true;
    this.dictionarySelected = false;
  }

  switchToDictionary(){
    this.filesSelected = false;
    this.dictionarySelected = true;
  }

}
