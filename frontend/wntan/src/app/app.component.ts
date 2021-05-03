import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {AppService} from './app.service';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(private _formbuilder: FormBuilder, private service: AppService) {
  }

  form: FormGroup;
  clusterSelected: string;
  clusterImgUrl: string;

  clusters = [];
  clustersSub: Subscription;
  clustersNames = [];

  countries = ["Ecuador", "Peru"]
  // countries = ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay", "Venezuela"]

  isProcessingSub: Subscription;

  isProcessing: boolean;

  ngOnInit(): void {
    this.form = this._formbuilder.group({
      country: [''],
      city: ['', [Validators.required]],
    })

    this.isProcessingSub = this.service.getIsProcessingListener().subscribe((resp) => {
      this.isProcessing = resp;
    })


    this.clustersSub = this.service.getClustersListener().subscribe((resp) => {
      this.clusters = resp;
      for (let c in this.clusters) {
        this.clustersNames.push(this.clusters[c]["cluster_name"])
      }
    })
  }

  onSubmit() {
    if(this.form.invalid){
      return
    }
    this.clusters = [];
    this.clustersNames = [];
    this.service.getClusters(this.form.value.country, this.form.value.city);
  }

  refresh(){
    this.clusters = [];
    this.clustersNames = [];
  }


  onSelectCluster() {
    for (let i in this.clusters) {
      if (this.clusters[i]["cluster_name"] === this.clusterSelected) {
        this.clusterImgUrl = this.clusters[i]["cluster_img"];
      }
    }
  }

}
