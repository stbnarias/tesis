import {Component, OnInit, ViewChild} from '@angular/core';
import { MetaboliteDictionaryService } from "./metabolite-dictionary.service";
import {MatPaginator, MatSort, MatTableDataSource} from "@angular/material";

@Component({
  selector: 'app-metabolite-dictionary',
  templateUrl: './metabolite-dictionary.component.html',
  styleUrls: ['./metabolite-dictionary.component.css'],
  providers: [MetaboliteDictionaryService]
})
export class MetaboliteDictionaryComponent implements OnInit {

  constructor(private service: MetaboliteDictionaryService) {
    this.service.getDictionary().subscribe( translations =>{
      this.translations = translations;
      this.translationsData = new MatTableDataSource<any>(translations as
        {_id: string, code: string, name: string, createdAt: Date, updatedAt: Date, __v: number}[]);
    });
  }

  translations: any = [];
  translationsData: MatTableDataSource<any>;
  displayedColumns: string[] = ['Code', 'Name', 'Created At', 'Actions'];
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {

    this.translationsData.sort = this.sort;
    this.translationsData.paginator = this.paginator;
  }

  deleteEntry(something){
    console.log(something);
  }



}
