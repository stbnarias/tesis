import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpRequest, HttpEvent } from '@angular/common/http'
import { map } from "rxjs/operators";
import { Observable } from 'rxjs';
import {Location} from "@angular/common";

@Injectable({
  providedIn: 'root'
})
export class KgmlFilesService {

  constructor(private http: HttpClient, private location:Location) { }

  getAllPathways(){ // TODO dynamic data using Observable type for return
    return this.http.get(this.location.prepareExternalUrl("/api/pathways")).pipe(map((files) => {
      return files;
    }));
  }

  uploadKGMLFileToDB(url: string, file: File):Observable<HttpEvent<any>>{
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

}
