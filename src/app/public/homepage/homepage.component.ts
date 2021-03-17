import {Location} from "@angular/common";

declare var require: any;
import {Component, OnInit, ViewChild, ElementRef} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {HomepageService} from './homepage.service';
import {Subscription} from 'rxjs';
import * as jsPDF from 'jspdf';
import {matDrawerAnimations} from '@angular/material';
import * as html2canvas from 'html2canvas';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css'],
  providers: [HomepageService]
})
export class HomepageComponent implements OnInit {

  constructor(private service: HomepageService, protected location: Location) {
    this.subscriptionType = service.getCurrentAlgorithmType().subscribe(type => {
      console.log("RECEIVING FROM SERVICE TYPE");
      console.log(type.text);
      this.currentAlgorithmTypeSelected = type.text;

    });
    this.subscriptionCode = service.getCurrentAlgorithmCode().subscribe(code => {
        console.log("RECEIVING FROM SERVICE CODE");
        console.log(code.code);
        this.currentAlgorithmCodeSelected = code.code;
      }
    );

    this.subscriptionGraph1 = service.getCurrentGraph1().subscribe(data => {
      console.log("RECEIVING FROM SERVICE GRAPH1");
      console.log(data);
      this.pathwayGraph1 = data.graph1;
      this.graph1Name = data.name;
      this.pathwayName1 = data.name;
      this.creatingGraph1 = false;
      this.startingNodeGraph1 = 0;
      this.endingNodeGraph1 = 0;

      let indexArgs = {"code": "GI", "name":this.pathwayName1, "graph": this.pathwayGraph1};
      this.callPython(indexArgs, this.service).then(indexes => {
        this.imagepathway1 = this.location.prepareExternalUrl('/images/' + this.pathwayName1 + '.png');
      });

      let args = {"code": "NIndex", "pathwayGraph": this.pathwayGraph1};
      this.callPython(args, this.service).then(indexes => {
        console.log("Indexes for this pathway1 are");
        console.log(indexes);
        this.pathwayNodes1 = [];
        for (const key in indexes["Nodes indexes"]) {
          if (indexes["Nodes indexes"].hasOwnProperty(key)) {
            this.pathwayNodes1.push({"index": key, "node": indexes["Nodes indexes"][key]});
          }
        }
        this.startingNodeGraph1 = 0;
        this.endingNodeGraph1 = 0;
      });

    });

    this.subscriptionGraph2 = service.getCurrentGraph2().subscribe(data => {
      console.log("RECEIVING FROM SERVICE GRAPH2");
      console.log(data);
      this.pathwayGraph2 = data.graph2;
      this.graph2Name = data.name;
      this.pathwayName2 = data.name;
      this.creatingGraph2 = false;
      this.startingNodeGraph2 = 0;
      this.endingNodeGraph2 = 0;

      let indexArgs = {"code": "GI", "name":this.pathwayName2, "graph": this.pathwayGraph2};
      this.callPython(indexArgs, this.service).then(indexes => {
        this.imagepathway2 = this.location.prepareExternalUrl('/images/' + this.pathwayName2 + '.png');
      });

      let args = {"code": "NIndex", "pathwayGraph": this.pathwayGraph2};
      this.callPython(args, this.service).then(indexes => {
        console.log("Indexes for this pathway2 are");
        console.log(indexes);
        this.pathwayNodes2 = [];
        for (const key in indexes["Nodes indexes"]) {
          if (indexes["Nodes indexes"].hasOwnProperty(key)) {
            this.pathwayNodes2.push({"index": key, "node": indexes["Nodes indexes"][key]});
          }
        }
        this.startingNodeGraph2 = 0;
        this.endingNodeGraph2 = 0;
      });

    });


  }

  @ViewChild('content') content: ElementRef;

  subscriptionType: Subscription;
  subscriptionCode: Subscription;
  subscriptionGraph1: Subscription;
  subscriptionGraph2: Subscription;
  anio: any;
  month: any;
  day: any;
  currentAlgorithmTypeSelected: any;
  currentAlgorithmCodeSelected: any;
  currentAlgorithmExecutionResult: any[];
  pathway1: File;
  pathway2: File;
  pathwayName1: string;
  pathwayName2: string;

  pathwayGraph1: any;
  pathwayGraph2: any;
  imagepathway1: string = "assets/images/negro.png";
  imagepathway2: string = "assets/images/negro.png";

  graph1Name: string;
  graph2Name: string;

  pathwayNodes1: any[];
  pathwayNodes2: any[];
  startingNodeGraph1: number;
  startingNodeGraph2: number;
  endingNodeGraph1: number;
  endingNodeGraph2: number;
  matchValue: number;
  missmatchValue: number;
  gapValue: number;

  isExtendedSelected: boolean;

  creatingGraph1: boolean;
  creatingGraph2: boolean;

  ngOnInit() {
    this.isExtendedSelected = false;
    this.currentAlgorithmTypeSelected = "Original";
    this.currentAlgorithmCodeSelected = "A1";
    this.isExtendedSelected = this.currentAlgorithmTypeSelected == "Extended";
    this.creatingGraph1 = false;
    this.creatingGraph2 = false;

    this.anio = new Date().getFullYear();
    this.month = new Date().getMonth() + 1;
    this.day = new Date().getDate();
    if (this.day < 10) {
      this.day = '0' + this.day.toString();
    }
    if (this.month < 10) {
      this.month = '0' + this.month.toString();
    }

  }

  createGraph1() {
    this.creatingGraph1 = true;
  }

  createGraph2() {
    this.creatingGraph2 = true;
  }

  processPathways() {
    function divideList(resultElement: any) {
      let result = "";
      let i: number;
      for (i = 0; i < resultElement.length - 1; i++) {
        result += resultElement[i] + "\n";
      }
      result += resultElement[i];
      return result;
    }

    function getCurrentAlgorithmExecutionResult(result: any) {
      let res = [];
      for (const key in result) {
        if (result.hasOwnProperty(key)) {
          // todo: mover esto a una variable global para usarlo multiples veces

          if (["Global BFT", "Local BFT", "SemiLocal BFT", "Global DFT", "Local DFT", "SemiLocal DFT"].includes(key)) {
            res.push({"key": key, "value": divideList(result[key])});
          } else {
            res.push({"key": key, "value": result[key]});
          }
        }
      }
      return res;
    }

    switch (this.currentAlgorithmTypeSelected) {
      case "Original":
        if (this.currentAlgorithmCodeSelected == 'A1') {

          this.matchValue = Number((<HTMLInputElement>document.getElementById("matchValue")).value);
          this.missmatchValue = Number((<HTMLInputElement>document.getElementById("mismatchValue")).value);
          this.gapValue = Number((<HTMLInputElement>document.getElementById("gapValue")).value);

          console.log("EXECUTING ALGORITHM A1");
          const originalArgs = {
            "code": this.currentAlgorithmCodeSelected,
            "pathwayGraph1": this.pathwayGraph1,
            "pathwayGraph2": this.pathwayGraph2,
            "match": this.matchValue,
            "missmatch": this.missmatchValue,
            "gap": this.gapValue
          };
          this.callPython(originalArgs, this.service).then(result => {
            console.log("RESULT FROM A1 ALGORITHM");
            this.currentAlgorithmExecutionResult = getCurrentAlgorithmExecutionResult(result);
            console.log(this.currentAlgorithmExecutionResult);
            //this.currentAlgorithmExecutionResult = Array.of(JSON.stringify(result));

          }).catch(error => {
            console.log("ERROR IN A1 ALGORITHM EXECUTION");
          });
        } else {
          if (this.currentAlgorithmCodeSelected == 'A2') {
            console.log("EXECUTING ALGORITHM A2");
            const originalArgs = {
              "code": this.currentAlgorithmCodeSelected,
              "pathwayGraph1": this.pathwayGraph1,
              "pathwayGraph2": this.pathwayGraph2
            };
            this.callPython(originalArgs, this.service).then(result => {
              console.log("RESULT FROM A2 ALGORITHM");
              this.currentAlgorithmExecutionResult = getCurrentAlgorithmExecutionResult(result);
              console.log(this.currentAlgorithmExecutionResult);
            }).catch(error => {
              console.log("ERROR IN A2 ALGORITHM EXECUTION");
            });
          } else {
            alert("Unknown code");
          }
        }
        break;
      case "Extended":
        this.matchValue = Number((<HTMLInputElement>document.getElementById("matchValue")).value);
        this.missmatchValue = Number((<HTMLInputElement>document.getElementById("mismatchValue")).value);
        this.gapValue = Number((<HTMLInputElement>document.getElementById("gapValue")).value);
        const extendedArgs = {
          "code": this.currentAlgorithmCodeSelected,
          "pathwayGraph1": this.pathwayGraph1,
          "pathwayGraph2": this.pathwayGraph2,
          "match": this.matchValue,
          "missmatch": this.missmatchValue,
          "gap": this.gapValue
        };
        switch (this.currentAlgorithmCodeSelected) {
          case 'A1T1':
            break;
          case 'A1T2':
            extendedArgs['startNodeGraph1'] = this.startingNodeGraph1;
            extendedArgs['startNodeGraph2'] = this.startingNodeGraph2;
            break;
          case 'A1T3':
            extendedArgs['startNodeGraph1'] = this.startingNodeGraph1;
            extendedArgs['startNodeGraph2'] = this.startingNodeGraph2;
            extendedArgs['endNodeGraph1'] = this.endingNodeGraph1;
            extendedArgs['endNodeGraph2'] = this.endingNodeGraph2;
            break;
          case 'A1T4':
            extendedArgs['startNodeGraph1'] = this.startingNodeGraph1;
            extendedArgs['startNodeGraph2'] = this.startingNodeGraph2;
            extendedArgs['endNodeGraph1'] = this.endingNodeGraph1;
            extendedArgs['endNodeGraph2'] = this.endingNodeGraph2;
            break;
          case 'A1T5':
            extendedArgs['startNodeGraph1'] = this.startingNodeGraph1;
            extendedArgs['startNodeGraph2'] = this.startingNodeGraph2;
            extendedArgs['endNodeGraph1'] = this.endingNodeGraph1;
            extendedArgs['endNodeGraph2'] = this.endingNodeGraph2;
            break;
        }
        this.callPython(extendedArgs, this.service).then(result => {
          console.log("RESULT FROM EXTENDED ALGORITHM");
          this.currentAlgorithmExecutionResult = getCurrentAlgorithmExecutionResult(result);
          console.log(this.currentAlgorithmExecutionResult);
          //this.currentAlgorithmExecutionResult = Array.of(JSON.stringify(result));

        }).catch(error => {
          console.log("ERROR IN EXTENDED ALGORITHM EXECUTION");
        });
        break;
      case "Weighted":
        alert("Not supported yet");
        break;
    }
  }

  savePathway1() {
    this.pathwaySaved(this.graph1Name, this.graph1Name, this.pathwayGraph1, this.graph1Name, this.service)
      .then(savedData => {
        console.log(savedData);
      });
  }

  savePathway2() {
    this.pathwaySaved(this.graph2Name, this.graph2Name, this.pathwayGraph2, this.graph2Name, this.service)
      .then(savedData => {
        console.log(savedData);
      });
  }

  async onSelectedFile(fileInput: any) {
    if (fileInput.target.files && fileInput.target.files[0]) {
      this.creatingGraph1 = false;
      this.pathway1 = fileInput.target.files[0];
      this.pathwayName1 = this.pathway1.name;
      console.log("Pathway1 name:");
      console.log(this.pathwayName1);
      this.fileUploaded(this.pathway1, this.service).then(filename => {
        this.graph1Name = filename as string;
        console.log("filename");
        console.log(filename);
        let args = {"code": "C1", "filename": filename + ".xml"};
        this.callPython(args, this.service).then(data => {
          console.log("RESULT FROM PYTHON");
          this.imagepathway1 = this.location.prepareExternalUrl('/images/' + filename + '.png');
          console.log(data["Compound Graph 1"]);
          this.pathwayGraph1 = JSON.stringify(data["Compound Graph 1"]);
          console.log("Calling NIndex Now for this Graph1");
          let indexArgs = {"code": "NIndex", "pathwayGraph": this.pathwayGraph1};
          this.callPython(indexArgs, this.service).then(indexes => {
            console.log("Indexes for this pathway1 are");
            console.log(indexes);
            this.pathwayNodes1 = [];
            for (const key in indexes["Nodes indexes"]) {
              if (indexes["Nodes indexes"].hasOwnProperty(key)) {
                this.pathwayNodes1.push({"index": key, "node": indexes["Nodes indexes"][key]});
              }
            }
            this.startingNodeGraph1 = 0;
            this.endingNodeGraph1 = 0;
          });
        });
      });
    }
  }

  public onSelectedFile2(fileInput: any) {
    if (fileInput.target.files && fileInput.target.files[0]) {
      this.creatingGraph2 = false;
      this.pathway2 = fileInput.target.files[0];
      this.pathwayName2 = this.pathway2.name;
      console.log("Pathway2 name:");
      console.log(this.pathwayName2);
      this.fileUploaded(this.pathway2, this.service).then(filename => {
        this.graph2Name = filename as string;
        console.log(filename);
        let args = {"code": "C1", "filename": filename + ".xml"};
        this.callPython(args, this.service).then(data => {
          console.log("RESULT FROM PYTHON");
          console.log(data["Compound Graph 1"]);
          this.imagepathway2 = this.location.prepareExternalUrl('/images/' + filename + '.png');
          this.pathwayGraph2 = JSON.stringify(data["Compound Graph 1"]);
          console.log("Calling NIndex Now for this Graph2");
          let indexArgs = {"code": "NIndex", "pathwayGraph": this.pathwayGraph2};
          this.callPython(indexArgs, this.service).then(indexes => {
            console.log("Indexes for this pathway2 are");
            console.log(indexes);
            this.pathwayNodes2 = [];
            for (const key in indexes["Nodes indexes"]) {
              if (indexes["Nodes indexes"].hasOwnProperty(key)) {
                this.pathwayNodes2.push({"index": key, "node": indexes["Nodes indexes"][key]});
              }
            }
            this.startingNodeGraph2 = 0;
            this.endingNodeGraph2 = 0;
          });
        });
      });
    }
    //this.imagepathway1 =  require("../../../../images/cit00710-1556089914716.png");
  }

  pathwaySaved = function (name, file, graph, image, providedService) {
    return new Promise((resolve, reject) => {
      providedService.savePathwayToDB(this.location.prepareExternalUrl("/api/pathways"), name, file, graph, image).subscribe(
        (data) => {
          if (data.body) {
            let key;
            for (key in data.body) {
              if (data.body.hasOwnProperty(key)) {
                resolve(data.body[key]);
              }
            }
          }
        }
      );
    });
  };

  callPython = function (args, providedService) {
    return new Promise((resolve, reject) => {
      providedService.callPython(args).subscribe(
        (data) => {
          if (data.body) {
            resolve(data.body);
          }
        }
      );
    });
  };

  fileUploaded = function (xmlFile, providedService) {
    return new Promise((resolve, reject) => {
        providedService.uploadXMLFile(this.location.prepareExternalUrl("/api/copyKGMLToTempUploads"), xmlFile).subscribe(
          (data) => {
            if (data.body) {
              var key;
              for (key in data.body) {
                if (data.body.hasOwnProperty(key)) {
                  resolve(data.body[key]);
                  //this.pathway1final = data.body[key];
                }
              }
            }
          });
      }
    );
  };

  setStartNodeGraph1(node) {
    this.startingNodeGraph1 = Number(node.target.value);
  }

  setStartNodeGraph2(node) {
    this.startingNodeGraph2 = Number(node.target.value);
  }

  setEndNodeGraph1(node) {
    this.endingNodeGraph1 = Number(node.target.value);
  }

  setEndNodeGraph2(node) {
    this.endingNodeGraph2 = Number(node.target.value);
  }

  downloadpdf() {
    const doc = new jsPDF();

    //imagen estatica
    var image = new Image();
    var width;
    var height;

    html2canvas(document.querySelector('#content')).then(canvas => {
      //logo del tec
      var logo = new Image();
      logo.src = "assets/images/logo-tec.png";
      doc.addImage(logo, "PNG", 165, 0, 40, 20);
      //titulo
      doc.text('Metabolic Pathways Comparison', 60, 30);

      //fecha
      doc.text("Date: " + this.anio + "-" + this.month + "-" + this.day, 10, 50);

      // todo: esto hay que cambiarlo por la dirección de la imagen generada
      image.src = "assets/images/negro.png";

      image.onload = function () {

        width = image.width;
        height = image.height;
        console.log(width);
        console.log(height);
        doc.addImage(image, "PNG", 5, 100, width / 10, height / 10);

        doc.addPage();
        doc.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, 211, 298);

        doc.save('Resultado.pdf');

      };


    });

  }
}
