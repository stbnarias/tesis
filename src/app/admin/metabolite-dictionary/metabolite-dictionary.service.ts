import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http'
import { map } from "rxjs/operators";
import {Location} from "@angular/common";

@Injectable({
  providedIn: 'root'
})
export class MetaboliteDictionaryService {

  constructor(private http: HttpClient, private location: Location) { }

  getDictionary() {
    return this.http.get(this.location.prepareExternalUrl("/api/translations/")).pipe(map((translations) => {
      return translations;
    }));
  }

}
