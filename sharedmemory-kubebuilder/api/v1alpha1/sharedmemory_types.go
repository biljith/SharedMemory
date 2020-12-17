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

package v1alpha1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// SharedmemorySpec defines the desired state of Sharedmemory
type SharedmemorySpec struct {
	// INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
	// Important: Run "make" to regenerate code after modifying this file

	// Foo is an example field of Sharedmemory. Edit Sharedmemory_types.go to remove/update
	Foo       string `json:"foo,omitempty"`
	TopicName string `json:"topicname,omitempty"`
	ShmSize   int    `json:"shmsize,omitempty"`
	MsgSize   int    `json:"msgsize,omitempty"`
}

// SharedmemoryStatus defines the observed state of Sharedmemory
type SharedmemoryStatus struct {
	// INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
	// Important: Run "make" to regenerate code after modifying this file
}

// +kubebuilder:object:root=true

// Sharedmemory is the Schema for the sharedmemories API
type Sharedmemory struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   SharedmemorySpec   `json:"spec,omitempty"`
	Status SharedmemoryStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// SharedmemoryList contains a list of Sharedmemory
type SharedmemoryList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Sharedmemory `json:"items"`
}

func init() {
	SchemeBuilder.Register(&Sharedmemory{}, &SharedmemoryList{})
}
