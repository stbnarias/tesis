import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpRequest, HttpEvent } from '@angular/common/http'
import { map } from "rxjs/operators";
import {Observable, Subject} from 'rxjs';
import {Location} from "@angular/common";

@Injectable({
  providedIn: 'root'
})
export class HomepageService {

  constructor(private http: HttpClient, private location: Location) { }

  private typeSubject = new Subject<any>();
  private codeSubject = new Subject<any>();
  private graph1Subject = new Subject<any>();
  private graph2Subject = new Subject<any>();

  setCurrentGraph2(graph: Object, graphName: string, origin: string){
    this.graph2Subject.next({graph2: graph, name: graphName, origin: origin});
  }

  getCurrentGraph2(): Observable<any>{
    return this.graph2Subject.asObservable();
  }

  setCurrentGraph1(graph: Object, graphName: string, origin: string){
    this.graph1Subject.next({graph1: graph, name: graphName, origin: origin});
  }

  getCurrentGraph1(): Observable<any>{
    return this.graph1Subject.asObservable();
  }

  getCurrentAlgorithmCode(): Observable<any>{
    return this.codeSubject.asObservable();
  }

  setCurrentAlgorithmCode(code: string) {
    this.codeSubject.next({ code: code });
  }

  getCurrentAlgorithmType(): Observable<any>{
    return this.typeSubject.asObservable();
  }

  setCurrentAlgorithmType(type: string) {
    this.typeSubject.next({ text: type });
  }


  savePathwayToDB(url: string, pathwayName: string, fileName: string, graph: Object, imageName: string):Observable<HttpEvent<any>>{
    let formData = new FormData();
    formData.append('name', pathwayName);
    if(fileName)
      formData.append('file', fileName +'.xml');
    formData.append('graph', JSON.stringify(graph));
    if(imageName)
      formData.append('image', imageName+'.png');

    let params = new HttpParams();

    const options = {
      params: params,
      reportProgress: true,
    };

    const req = new HttpRequest('POST', url, formData, options);
    return this.http.request(req);
  }

  uploadXMLFile(url: string, file: File):Observable<HttpEvent<any>>{
    let formData = new FormData();
    formData.append('file', file);

    let params = new HttpParams();

    const options = {
      params: params,
      reportProgress: true,
    };

    const req = new HttpRequest('POST', url, formData, options);
    return this.http.request(req);
  }

  callPython(args: object):Observable<HttpEvent<any>>{ //url: string, filename: string, code: string
    let url = this.location.prepareExternalUrl("/api/python");
    let formData = new FormData();

    const algorithmCodes = ["A1", "A1T1", "A1T2", "A1T3", "A1T4", "A1T5", "A2"]; //TODO check for A2
    if(algorithmCodes.includes(args['code'])){
      console.log('FINAL CHECK BE4 EXEC ALGORITHMS FOR PATHWAYS GRAPHS');
      console.log(args['pathwayGraph1']);
      console.log(args['pathwayGraph2']);
      formData.append('pathwayGraph1', args['pathwayGraph1']);
      formData.append('pathwayGraph2', args['pathwayGraph2']);
      switch (args['code']) {
        case 'A1':
          formData.append('match', args['match']);
          formData.append('missmatch', args['missmatch']);
          formData.append('gap', args['gap']);
          formData.append('code', args['code']);
          break;
        case 'A1T1':
          formData.append('match', args['match']);
          formData.append('missmatch', args['missmatch']);
          formData.append('gap', args['gap']);
          formData.append('code', args['code']);
          break;
        case 'A1T2':
          formData.append('startNodeGraph1', args['startNodeGraph1']);
          formData.append('startNodeGraph2', args['startNodeGraph2']);
          formData.append('match', args['match']);
          formData.append('missmatch', args['missmatch']);
          formData.append('gap', args['gap']);
          formData.append('code', args['code']);
          break;
        case 'A1T3':
          formData.append('startNodeGraph1', args['startNodeGraph1']);
          formData.append('startNodeGraph2', args['startNodeGraph2']);
          formData.append('endNodeGraph1', args['endNodeGraph1']);
          formData.append('endNodeGraph2', args['endNodeGraph2']);
          formData.append('match', args['match']);
          formData.append('missmatch', args['missmatch']);
          formData.append('gap', args['gap']);
          formData.append('code', args['code']);
          break;
        case 'A1T4':
          formData.append('startNodeGraph1', args['startNodeGraph1']);
          formData.append('startNodeGraph2', args['startNodeGraph2']);
          formData.append('endNodeGraph1', args['endNodeGraph1']);
          formData.append('endNodeGraph2', args['endNodeGraph2']);
          formData.append('match', args['match']);
          formData.append('missmatch', args['missmatch']);
          formData.append('gap', args['gap']);
          formData.append('code', args['code']);
          break;
        case 'A1T5':
          formData.append('endNodeGraph1', args['endNodeGraph1']);
          formData.append('endNodeGraph2', args['endNodeGraph2']);
          formData.append('match', args['match']);
          formData.append('missmatch', args['missmatch']);
          formData.append('gap', args['gap']);
          formData.append('code', args['code']);
          break;
        case 'A2':
          formData.append('code', args['code']);
          break;
      }
    }
    if(['C1'].includes(args['code'])){
      formData.append('filename', args['filename']);
      formData.append('code', args['code']);
    }

    if(['NIndex'].includes(args['code'])){
      console.log(args['pathwayGraph']);
      formData.append('pathwayGraph', args['pathwayGraph']);
      formData.append('code', args['code']);
    }
    if(['GI'].includes(args['code'])){
      formData.append('name', args['name']);
      formData.append('graph', args['graph']);
      formData.append('code', args['code']);
    }
    let params = new HttpParams();//.set('filename', file);
    //params.append('code', code);

    const options = {
      params: params, reportProgress: true,
    };

    const req = new HttpRequest('POST', url, formData, options);

    const data = this.http.request(req);
    // console.log("HELLO FROM HOMEPAGE.SERVICE (PYTHON)");
    return data;
  }
}
