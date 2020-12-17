/*
Copyright 2020 Biljith Thadichi.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controllers

import (
	"context"
	"io/ioutil"
	"net/http"
	"strconv"

	"github.com/go-logr/logr"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	isv1alpha1 "sharedmemory-kubebuilder/api/v1alpha1"
)

// SharedmemoryReconciler reconciles a Sharedmemory object
type SharedmemoryReconciler struct {
	client.Client
	Log    logr.Logger
	Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=is.github.com,resources=sharedmemories,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=is.github.com,resources=sharedmemories/status,verbs=get;update;patch

func (r *SharedmemoryReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	_ = context.Background()
	reqLogger := r.Log.WithValues("sharedmemory", req.NamespacedName)
	reqLogger.Info("In reconciler")

	// Get the CRD instance
	instance := &isv1alpha1.Sharedmemory{}
	err := r.Get(context.TODO(), req.NamespacedName, instance)

	if err != nil {
		if errors.IsNotFound(err) {
			return ctrl.Result{}, nil
		}
		return ctrl.Result{}, err
	}

	reqLogger.Info(instance.Spec.Foo)
	reqLogger.Info(instance.Spec.TopicName)
	reqLogger.Info(strconv.Itoa(instance.Spec.ShmSize))
	reqLogger.Info(strconv.Itoa(instance.Spec.MsgSize))

	resp, err := http.Get("http://10.98.89.208:6969/createTopic/" +
		instance.Spec.TopicName +
		"/" +
		strconv.Itoa(instance.Spec.ShmSize) +
		"/" +
		strconv.Itoa(instance.Spec.MsgSize))
	if err != nil {
		return ctrl.Result{}, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return ctrl.Result{}, err
	}
	reqLogger.Info(string(body))

	return ctrl.Result{}, nil
}

func (r *SharedmemoryReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&isv1alpha1.Sharedmemory{}).
		Complete(r)
}
