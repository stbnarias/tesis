import { Component, OnInit, Input } from '@angular/core';
import { HomepageService } from '../homepage.service';

@Component({
  selector: 'app-pathway-image-view',
  templateUrl: './pathway-image-view.component.html',
  styleUrls: ['./pathway-image-view.component.css']
})
export class PathwayImageViewComponent implements OnInit {

  @Input() imagepathway1:string;
  @Input() imagepathway2:string;
  constructor(private service: HomepageService) { }

  ngOnInit() {
    $(document).ready( function() {
      $("#filter-bar2 li").click(function(){
        $("#filter-bar2 li").removeClass("active");
        $(this).addClass("active");
        $("#filter-bar2").removeClass().addClass($(this).attr("data-target"));
      });
    });
  }

  checkCurrentValue(value){
    alert(value);
  }

  changeImageView(currentView: string) {
    //alert(currentView);
    if(currentView === 'name'){
      //enviar name
      console.log("name");
    }else{
      //enviar code
      console.log("code");
    }
  }


}
